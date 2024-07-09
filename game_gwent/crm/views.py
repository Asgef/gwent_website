from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from game_gwent.mixins import (
    ExtraContextMixin, CartDetailMixin
)
from .forms import UserForm, AddressForm, OrderForm
from django.conf import settings
from .models import OrderItem, User, Address
import uuid
from yookassa import Configuration, Payment
import os

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

class OrderDetailView(
    ExtraContextMixin, CartDetailMixin, FormView
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
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST)
        address_form = AddressForm(self.request.POST)

        if user_form.is_valid() and address_form.is_valid():
            user_data = user_form.cleaned_data
            address_data = address_form.cleaned_data

            # Создаём или пере используем пользователя и адрес
            user, created_user = User.objects.get_or_create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                patronymic=user_data['patronymic'],
                phone_num=user_data['phone_num'],
                email=user_data['email'],
            )

            address, created_address = Address.objects.get_or_create(
                region=address_data['region'],
                city=address_data['city'],
                street=address_data['street'],
                house=address_data['house'],
                apt=address_data['apt'],
                postal_code=address_data['postal_code'],
            )

            # Сохраняем заказ без записи в БД
            order = form.save(commit=False)
            order.customer = user
            order.address = address

            # Получаем элементы корзины и общую сумму
            cart_items, total = self.get_cart_items()

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

    def create_yookassa_payment(self, order, total_price):
        idempotence_key = uuid.uuid4()

        if settings.DEBUG:
            return_url = f"{settings.NGROK_URL}{reverse_lazy('payment_success')}"
            if not return_url:
                raise ValueError(
                    "При локальной разработке следует запустить ngrok"
                )
        else:
            return_url = self.request.build_absolute_uri(
                reverse_lazy('payment_success')
            )

        payment = Payment.create({
            "amount": {
                "value": f"{total_price:.2f}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": f"Оплата заказа №{order.id}"
        }, idempotence_key)

        return payment.confirmation.confirmation_url


def payment_success(request):
    return HttpResponse("Платеж успешно завершен.")
