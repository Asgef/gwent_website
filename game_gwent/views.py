from django.views.generic import ListView, TemplateView
from game_gwent.catalog.models import Product, ProductImage
from .mixins import ExtraContextMixin, CartStatusMixin


class HomeListView(ExtraContextMixin, CartStatusMixin, ListView):
    model = Product
    template_name = 'home_page.html'

    extra_context = {
        'title': 'WooGames',
        'greeting_title': 'Приключения | Азарт | Непотребства',
        'greeting_description': 'Древесина твердых пород, собранная со всего'
                                'мира, тщательно обработанная в'
                                'высококачественные изделия для бла бла бла',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            product.gallery_image = ProductImage.objects.filter(
                product=product
            ).first()
        return context


class AboutPageView(ExtraContextMixin, CartStatusMixin, TemplateView):
    template_name = 'about.html'
    extra_context = {
        'title': 'О нас'
    }


class ContactPageView(ExtraContextMixin, CartStatusMixin, TemplateView):
    template_name = 'contact.html'
    extra_context = {
        'title': 'Связь с нами'
    }
