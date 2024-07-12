from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from game_gwent.mixins import (
    ExtraContextMixin, PaymentOrderMixin, BuyNowDetailMixin, CartItemMixin,
    CartStatusMixin
)
from .forms import UserForm, AddressForm, OrderForm
from django.conf import settings
from .models import OrderItem, User, Address
from yookassa import Configuration

from ..catalog.models import Product

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class CartOrderlView(
    ExtraContextMixin, PaymentOrderMixin, CartItemMixin, FormView
):
    template_name = 'crm/order.html'
    form_class = OrderForm
    extra_context = {
        'title': 'Оформление заказа',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total = self.get_cart_items()

        context['cart_items'] = cart_items
        context['total'] = total
        context['user_form'] = UserForm(self.request.POST or None)
        context['address_form'] = AddressForm(self.request.POST or None)
        context['order_form'] = OrderForm(self.request.POST or None)
        context['DADATA_API_KEY'] = settings.DADATA_API_KEY
        return context  # ушло в шаблон

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)
        address_form = AddressForm(self.request.POST)
        action = self.request.POST.get('action')
        free_shipping = self.request.POST.get('free_shipping', 'on') == 'on'

        if user_form.is_valid():
            user_data = user_form.cleaned_data

            # Создаём или пере используем пользователя и адрес
            user, created_user = User.objects.get_or_create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                patronymic=user_data['patronymic'],
                phone_num=user_data['phone_num'],
                email=user_data['email'],
            )

            if action == 'checkout':  # ручная обработка заказа
                address, created_address = Address.objects.get_or_create(
                    is_manual=True,
                    defaults={
                        'region': '', 'city': '', 'street': '',
                        'house': '', 'apt': '', 'postal_code': ''
                    }
                )
            else:  # обработка заказа с адресом
                if address_form.is_valid():
                    address_data = address_form.cleaned_data
                    address, created_address = Address.objects.get_or_create(
                        region=address_data['region'],
                        city=address_data['city'],
                        street=address_data['street'],
                        defaults={
                            'house': address_data['house'],
                            'apt': address_data['apt'],
                            'postal_code': address_data['postal_code'],
                            'is_manual': False
                        }
                    )
                else:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form, user_form=user_form,
                            address_form=address_form
                        )
                    )

            # Сохраняем заказ без записи в БД
            order = form.save(commit=False)
            order.customer = user
            order.address = address

            # Получаем элементы заказа и общую сумму
            cart_items, total = self.get_cart_items()
            print(f'Получаем элементы заказа и общую сумму {cart_items}, {total}')

            # Устанавливаем total_price перед сохранением заказа
            order.total_price = total
            order.save()

            # Создаем OrderItem для каждого товара в корзине
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    product_price_at_order=item['product'].price
                )

            # Очищаем корзину
            self.request.session['cart'] = {}

            if action == 'checkout':
                return redirect('order_processed')
            else:
                # Создаём платёж через Yookassa
                payment = self.create_yookassa_payment(order, total)
                return redirect(payment)

        # Если форма не валидна, возвращаем данные формы
        # TODO: Реализовать флеш сообщения
        return self.render_to_response(
            self.get_context_data(
                form=form, user_form=user_form, address_form=address_form
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BuyNowOrderView(ExtraContextMixin, CartStatusMixin, BuyNowDetailMixin, PaymentOrderMixin, FormView):
    template_name = 'crm/order.html'
    form_class = OrderForm
    extra_context = {
        'title': 'Быстрая покупка',
    }

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and 'quantity' in request.POST:
            self.product_id = kwargs.get('pk')
            self.quantity = int(request.POST.get('quantity', 1))
            request.session['buy_now'] = {
                'product_id': self.product_id,
                'quantity': self.quantity,
            }
            return redirect('buy_now', pk=self.product_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'buy_now' in self.request.session:
            product_data = self.request.session['buy_now']
            product = get_object_or_404(Product, id=product_data['product_id'])
            buy_now_items = [{
                'product': product,
                'quantity': product_data['quantity'],
                'total_price': product.price * product_data['quantity']
            }]
            total = buy_now_items[0]['total_price']
            context['buy_now_items'] = buy_now_items
            context['total'] = total
        else:
            # Handle case when 'buy_now' is not in session
            context['buy_now_items'] = []
            context['total'] = 0

        if self.request.method == 'POST':
            context['user_form'] = UserForm(self.request.POST)
            context['address_form'] = AddressForm(self.request.POST)
            context['order_form'] = OrderForm(self.request.POST)
        else:
            context['user_form'] = UserForm()
            context['address_form'] = AddressForm()
            context['order_form'] = OrderForm()
        context['DADATA_API_KEY'] = settings.DADATA_API_KEY
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)
        address_form = AddressForm(self.request.POST)
        action = self.request.POST.get('action')
        free_shipping = self.request.POST.get('free_shipping', 'on') == 'on'

        if user_form.is_valid():
            user_data = user_form.cleaned_data

            # Создаём или пере используем пользователя и адрес
            user, created_user = User.objects.get_or_create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                patronymic=user_data['patronymic'],
                phone_num=user_data['phone_num'],
                email=user_data['email'],
            )

            if action == 'checkout':  # ручная обработка заказа
                address, created_address = Address.objects.get_or_create(
                    is_manual=True,
                    defaults={
                        'region': '', 'city': '', 'street': '',
                        'house': '', 'apt': '', 'postal_code': ''
                    }
                )
            else:  # обработка заказа с адресом
                if address_form.is_valid():
                    address_data = address_form.cleaned_data
                    address, created_address = Address.objects.get_or_create(
                        region=address_data['region'],
                        city=address_data['city'],
                        street=address_data['street'],
                        defaults={
                            'house': address_data['house'],
                            'apt': address_data['apt'],
                            'postal_code': address_data['postal_code'],
                            'is_manual': False
                        }
                    )
                else:
                    return self.render_to_response(
                        self.get_context_data(
                            form=form, user_form=user_form,
                            address_form=address_form
                        )
                    )

            # Сохраняем заказ без записи в БД
            order = form.save(commit=False)
            order.customer = user
            order.address = address

            # Получаем элементы заказа и общую сумму
            buy_now_items, total = self.get_buy_now_items()

            # Устанавливаем total_price перед сохранением заказа
            order.total_price = total
            order.save()

            # Создаем OrderItem для каждого товара в корзине
            for item in buy_now_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    product_price_at_order=item['product'].price
                )

            if action == 'checkout':
                return redirect('order_processed')
            else:
                # Создаём платёж через Yookassa
                payment = self.create_yookassa_payment(order, total)
                return redirect(payment)

        return self.render_to_response(
            self.get_context_data(
                form=form, user_form=user_form, address_form=address_form
            )
        )

    def post(self, request, *args, **kwargs):
        if 'buy_now' in request.session:
            self.product_id = request.session['buy_now']['product_id']
            self.quantity = request.session['buy_now']['quantity']
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class OrderProcessedView(ExtraContextMixin, TemplateView):
    template_name = 'crm/order_processed.html'
    extra_context = {
        'title': 'Спасибо, мы с вами свяжемся',
    }


class SuccessPageView(ExtraContextMixin, TemplateView):
    template_name = 'crm/payment_success.html'
    extra_context = {
        'title': 'Успешный заказ',
    }


class BuyOrderlView(ExtraContextMixin, PaymentOrderMixin, BuyNowDetailMixin, FormView):
    template_name = 'crm/order.html'
    form_class = OrderForm
    extra_context = {
        'title': 'Оформление заказа',
    }
