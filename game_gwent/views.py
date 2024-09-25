from django.views.generic import ListView, TemplateView
from game_gwent.catalog.models import Product, ProductImage
from .mixins import ExtraContextMixin, CartStatusMixin


class HomeListView(ExtraContextMixin, CartStatusMixin, ListView):
    model = Product
    template_name = 'home_page.html'

    extra_context = {
        'title': 'WooGames',
        'greeting_title': 'Добро пожаловать в мир настольных приключений!',
        'greeting_description': (
            'Откройте для себя лучшие настольные игры'
            'для всех возрастов и интересов — от стратегий до квестов. '
            'Погрузитесь в захватывающие вселенные, соберите друзей и создайте '
            'незабываемые истории за игровым столом.'
        ),
        'stor_description': 'В нашем магазине вы найдете всё необходимое для весёлых вечеров и эпических баталий!'
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
