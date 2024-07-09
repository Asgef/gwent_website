import json
from django.http import HttpResponse
from game_gwent.crm.models import Order
from yookassa.domain.common import SecurityHelper
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import (
    WebhookNotificationEventType, WebhookNotificationFactory
)


@csrf_exempt
def yookassa_webhook(request):  # noqa C901
    # Если хотите убедиться, что запрос пришел от ЮКасса, добавьте проверку:
    ip = get_client_ip(request)  # Получите IP запроса
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    # Извлечение JSON объекта из тела запроса
    event_json = json.loads(request.body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object

        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:  # noqa: E501
            order_id = response_object.metadata.get('order_id')
            print(f'ORDER_ID = {order_id}')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.paid = True
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponse(status=404)

        # Другие типы уведомлений
        # ...

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо


def get_client_ip(request):
    """ Helper function to get client IP address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
