from django.views.generic import TemplateView


class IndexView(TemplateView):  # noqa: D101
    template_name = 'home_page.html'
    extra_context = {
        'title': 'Gwent',
    }
