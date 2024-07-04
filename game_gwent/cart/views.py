from django.shortcuts import redirect
from django.urls import reverse
from game_gwent.catalog.models import Product
from django.views.generic import ListView
from game_gwent.mixins import (
    ExtraContextMixin, CartStatusMixin, CartDetailMixin
)
from django.views import View


class CartListView(
    ExtraContextMixin, CartStatusMixin, CartDetailMixin, ListView
):
    model = Product
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'
    extra_context = {
        'title': 'Корзина',
    }


class AddToCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        if str(pk) in cart:
            cart[str(pk)] += quantity
        else:
            cart[str(pk)] = quantity
        request.session['cart'] = cart
        return redirect(reverse('cart_detail'))


class RemoveFromCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        if str(pk) in cart:
            del cart[str(pk)]
            request.session['cart'] = cart
        return redirect(reverse('cart_detail'))


class UpdateCartView(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        action = request.POST.get('action')

        product = Product.objects.get(id=pk)
        min_quantity = 1
        max_quantity = product.stock

        if action == 'increase' and cart[str(pk)] < max_quantity:
            cart[str(pk)] += 1
        elif action == 'decrease' and cart[str(pk)] > min_quantity:
            cart[str(pk)] -= 1

        request.session['cart'] = cart
        return redirect(reverse('cart_detail'))

    # TODO: Доработать добавление товара в корзину.
