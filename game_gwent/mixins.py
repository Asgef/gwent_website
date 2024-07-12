import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from yookassa import Payment
from game_gwent.catalog.models import Product


class ExtraContextMixin:  # noqa: D101
    def get_extra_context(self):
        return {
            'phn_number': '+725762976',
            'email': 'enter@ent.com',
        }

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)
        extra_context = self.get_extra_context()
        view_extra_context = getattr(self, 'extra_context', {})
        if not isinstance(view_extra_context, dict):
            view_extra_context = {}

        extra_context.update(view_extra_context)
        context.update(extra_context)
        return context


# TODO: Вынести данные в константы


class CartStatusMixin:  # noqa: D101
    def get_cart_status(self):  # noqa: D102
        cart = self.request.session.get('cart', {})
        return 'filled' if cart else 'empty'

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)
        context['cart_status'] = self.get_cart_status()
        return context


class CartItemMixin:
    def get_cart_items(self):  # noqa: D102
        cart = self.request.session.get('cart', {})
        cart_items = []
        total = 0

        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            quantity = cart[str(product.id)]
            total += product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
        return cart_items, total


class CartDetailMixin(CartItemMixin):  # noqa: D101
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total = self.get_cart_items()
        context['cart_items'] = cart_items
        context['total'] = total
        return context


class BuyNowDetailMixin:  # noqa: D101
    def get_buy_now_items(self):  # noqa: D102
        product_data = self.request.session['buy_now']
        product = get_object_or_404(Product, id=product_data['product_id'])
        buy_now_items = [{
            'product': product,
            'quantity': product_data['quantity'],
            'total_price': product.price * int(product_data['quantity'])
        }]
        total = buy_now_items[0]['total_price']

        return buy_now_items, total

# class OrderDetailMixin(CartDetailMixin, BuyNowDetailMixin):  # noqa: D101
#     def get_items(self):
#         if 'buy_now' in self.request.session:
#             return self.get_buy_now_items()
#         return self.get_cart_items()


class PaymentOrderMixin:
    def create_yookassa_payment(self, order, total_price):
        idempotence_key = uuid.uuid4()

        if not settings.PRODUCTION:
            ngrok_url = settings.NGROK_URL
            if not ngrok_url:
                raise ValueError(
                    "При локальной разработке следует запустить ngrok"
                )
            return_url = f"{ngrok_url}{reverse_lazy('payment_success')}"
        else:
            return_url = self.request.build_absolute_uri(
                reverse_lazy('payment_success')
            )

        payment = Payment.create({
            "amount": {
                "value": f"{total_price:.2f}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": f"Оплата заказа №{order.id}",
            "metadata": {
                "order_id": str(order.id)
            }
        }, idempotence_key)

        return payment.confirmation.confirmation_url
