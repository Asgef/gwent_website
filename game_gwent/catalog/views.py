from django.views.generic import DetailView
from .models import Product
from game_gwent.mixins import ExtraContextMixin, CartStatusMixin


class CatalogDetailView(ExtraContextMixin, CartStatusMixin, DetailView):
    model = Product
    template_name = 'catalog/product_show.html'

# TODO: определить содержимое extra_context
