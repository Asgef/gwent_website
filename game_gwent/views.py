from django.views.generic import TemplateView


class IndexView(TemplateView):  # noqa: D101
    template_name = 'index.html'
    extra_context = {
        'title': 'Gwent',
    }
