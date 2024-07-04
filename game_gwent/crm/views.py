from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from game_gwent.catalog.models import Product
from django.views.generic import TemplateView
from game_gwent.mixins import (
    ExtraContextMixin, CartStatusMixin, CartDetailMixin
)
from .forms import UserForm, AdressForm, OrderForm
from django.conf import settings
from .models import User, Address, Order, OrderItem
from django.views import View


class OrderDetailView(
    ExtraContextMixin, CartStatusMixin, CartDetailMixin, TemplateView
):
    model = Product
    template_name = 'crm/order.html'
    context_object_name = 'order'
    extra_context = {
        'title': 'Оформление заказа',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total = self.get_cart_items()
        context['cart_items'] = cart_items
        context['total'] = total
        context['user_form'] = UserForm()
        context['address_form'] = AdressForm()
        context['order_form'] = OrderForm(initial={'total_price': total})
        context['DADATA_API_KEY'] = settings.DADATA_API_KEY
        return context
#
#
#
# class AddToCartView(View):
#     def post(self, request, pk):
#         cart = request.session.get('cart', {})
#         quantity = int(request.POST.get('quantity', 1))
#         if str(pk) in cart:
#             cart[str(pk)] += quantity
#         else:
#             cart[str(pk)] = quantity
#         request.session['cart'] = cart
#         return redirect(reverse('cart_detail'))
#
#
# class RemoveFromCartView(View):
#     def post(self, request, pk):
#         cart = request.session.get('cart', {})
#         if str(pk) in cart:
#             del cart[str(pk)]
#             request.session['cart'] = cart
#         return redirect(reverse('cart_detail'))
#
#
# class UpdateCartView(View):
#     def post(self, request, pk):
#         cart = request.session.get('cart', {})
#         action = request.POST.get('action')
#
#         product = Product.objects.get(id=pk)
#         min_quantity = 1
#         max_quantity = product.stock
#
#         if action == 'increase' and cart[str(pk)] < max_quantity:
#             cart[str(pk)] += 1
#         elif action == 'decrease' and cart[str(pk)] > min_quantity:
#             cart[str(pk)] -= 1
#
#         request.session['cart'] = cart
#         return redirect(reverse('cart_detail'))
#
#     # TODO: Доработать добавление товара в корзину.
#
