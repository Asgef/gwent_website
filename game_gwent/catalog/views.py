from django.views.generic import DetailView
from .models import Product


class CatalogDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_show.html'
    extra_context = {
        'title': 'Product',
        'button_text': 'Show'
    }
# TODO: определить содержимое extra_context
