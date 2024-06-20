from django.urls import path
from .views import cart_detail, add_to_cart, remove_from_cart, update_cart


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path(
        'cart/remove/<int:product_id>/', remove_from_cart,
        name='remove_from_cart'
    ),
    path(
        'cart/update/<int:product_id>/<int:quantity>/', update_cart,
        name='update_cart'
    ),
]
