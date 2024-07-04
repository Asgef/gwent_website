from django.urls import path
from .views import OrderDetailView


urlpatterns = [
    path(
        '', OrderDetailView.as_view(),
        name='add_order'
    ),
]
