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


class CartDetailMixin:  # noqa: D101
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total = self.get_cart_items()
        context['cart_items'] = cart_items
        context['total'] = total
        return context
