from django.urls import path
from .views import OrderDetailView, SuccessPageView, OrderProcessedView
from .webhooks import yookassa_webhook


urlpatterns = [

    path(
        '', OrderDetailView.as_view(),
        name='add_order'
    ),
    path(
        'payment_success', SuccessPageView.as_view(),
        name='payment_success'
    ),
    path(
        'verify', yookassa_webhook,
        name='verify'
    ),
    path(
        'order/processed/', OrderProcessedView.as_view(),
        name='order_processed'
    ),

]
