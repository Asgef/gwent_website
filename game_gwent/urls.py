"""URL configuration for game_gwent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import HomeListView, AboutPageView, ContactPageView
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', HomeListView.as_view(), name='home_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('collections/', include('game_gwent.catalog.urls')),
    path('cart/', include('game_gwent.cart.urls')),
    path('checkouts/', include('game_gwent.crm.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
