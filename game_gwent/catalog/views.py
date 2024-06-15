from django.views.generic import ListView
from .models import Product


class CatalogListView(ListView):
    model = Product
    template_name = 'catalog/product.html'

