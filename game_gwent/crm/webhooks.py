from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order


# @csrf_exempt
# def yoocassa_webhoock(requests):
#
