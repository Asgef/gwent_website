from django.shortcuts import render, redirect
from django.urls import reverse
from game_gwent.catalog.models import Product


def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        total += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    return render(
        request, 'cart/cart.html', {
            'cart_items': cart_items, 'total': total
        }
    )


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect(reverse('cart_detail'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect(reverse('cart_detail'))


def update_cart(request, product_id, quantity):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] = quantity
        request.session['cart'] = cart

    return redirect(reverse('cart_detail'))
