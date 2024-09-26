from django.views.generic import DetailView
from .models import Product, ProductImage
from game_gwent.mixins import ExtraContextMixin, CartStatusMixin


class CatalogDetailView(ExtraContextMixin, CartStatusMixin, DetailView):
    
    model = Product
    template_name = 'catalog/product_show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object)
        return context

# TODO: определить содержимое extra_context
