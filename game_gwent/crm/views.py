from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from game_gwent.mixins import (
    ExtraContextMixin, CartDetailMixin
)
from .forms import UserForm, AddressForm, OrderForm
from django.conf import settings
from .models import Order, OrderItem


class OrderDetailView(
    ExtraContextMixin, CartDetailMixin, CreateView
):
    model = Order
    form_class = OrderForm
    template_name = 'crm/order.html'
    context_object_name = 'order'
    extra_context = {
        'title': 'Оформление заказа',
    }
    # success_url = reverse_lazy('order_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total = self.get_cart_items()
        context['cart_items'] = cart_items
        context['total'] = total
        context['user_form'] = UserForm(self.request.POST or None)
        context['address_form'] = AddressForm(self.request.POST or None)
        context['order_form'] = OrderForm(
            initial={'total_price': total},
            data=self.request.POST or None
        )
        context['DADATA_API_KEY'] = settings.DADATA_API_KEY
        return context

    def post(self, request, *args, **kwargs):
        user_forms = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        order_form = OrderForm(request.POST)

        forms = [
            user_forms.is_valid(), address_form.is_valid(),
            order_form.is_valid()
        ]

        if all(forms):
            user = user_forms.save()
            address = address_form.save()
            order = order_form.save(commit=False)
            order.customer = user
            order.address = address

            cart_items, total = self.get_cart_items()
            order.total_price = total
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )

            request.session['cart'] = {}

            return redirect(
                reverse_lazy(
                    'payment_page', kwargs={
                        'order_id': order.id, 'amount': order.total_price
                    }
                )
            )
        return self.render_to_response(self.get_context_data())
