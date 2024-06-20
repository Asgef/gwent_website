from django.urls import path
from .views import CatalogDetailView


urlpatterns = [
    path(
        '<int:pk>/', CatalogDetailView.as_view(),
        name='collections_detail'
    ),
]
