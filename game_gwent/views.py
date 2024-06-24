from django.views.generic import ListView, TemplateView
from game_gwent.catalog.models import Product
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


class AboutPageView(ExtraContextMixin, CartStatusMixin, TemplateView):
    template_name = 'about.html'
    extra_context = {
        'title': 'О нас'
    }
