from django.views.generic import ListView
from game_gwent.catalog.models import Product


class HomeListView(ListView):
    model = Product
    template_name = 'home_page.html'

