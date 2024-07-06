from django.urls import path
from .views import OrderDetailView, payment_placeholder


urlpatterns = [
    path(
        '', OrderDetailView.as_view(),
        name='add_order'
    ),
    path(
        'payment_placeholder/<int:order_id>/',
        payment_placeholder, name='payment_placeholder'
    ),

]
