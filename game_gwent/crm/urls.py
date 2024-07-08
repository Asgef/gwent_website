from django.urls import path
from .views import OrderDetailView, payment_success


urlpatterns = [
    path(
        '', OrderDetailView.as_view(),
        name='add_order'
    ),
path(
        'payment_success', payment_success,
        name='payment_success'
    ),

]
