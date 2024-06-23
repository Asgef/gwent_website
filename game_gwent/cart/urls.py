from django.urls import path
from .views import CartListView, AddToCartView, RemoveFromCartView, UpdateCartView

urlpatterns = [
    path('', CartListView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path(
        'remove/<int:pk>/', RemoveFromCartView.as_view(),
        name='remove_from_cart'
    ),
    path(
        'update/<int:pk>/', UpdateCartView.as_view(),
        name='update_cart'
    ),
]
