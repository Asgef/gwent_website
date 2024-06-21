from django.urls import path
from .views import cart_detail, add_to_cart, remove_from_cart, update_cart


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:pk>/', add_to_cart, name='add_to_cart'),
    path(
        'remove/<int:pk>/', remove_from_cart,
        name='remove_from_cart'
    ),
    path(
        'update/<int:pk>/', update_cart,
        name='update_cart'
    ),
]
