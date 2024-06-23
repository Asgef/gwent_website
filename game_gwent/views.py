from django.views.generic import ListView
from game_gwent.catalog.models import Product
from .mixins import ExtraContextMixin


class HomeListView(ExtraContextMixin, ListView):
    model = Product
    template_name = 'home_page.html'

    extra_context = {
        'title': 'WooGames',
        'greeting_title': 'Приключения | Азарт | Непотребства',
        'greeting_description': 'Древесина твердых пород, собранная со всего'
                                'мира, тщательно обработанная в'
                                'высококачественные изделия для бла бла бла',
    }
