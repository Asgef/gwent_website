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


def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))
    if str(pk) in cart:
        cart[str(pk)] += quantity
    else:
        cart[str(pk)] = quantity
    request.session['cart'] = cart
    return redirect(reverse('cart_detail'))


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart

    return redirect(reverse('cart_detail'))


def update_cart(request, pk):

    print("POST data:", request.POST)
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
