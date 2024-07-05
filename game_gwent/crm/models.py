from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from game_gwent.catalog.models import Product


class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    phone_num = PhoneNumberField(region='RU', verbose_name="Номер телефона")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    region = models.CharField(max_length=100, verbose_name="Область")
    city = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Город / Населенный пункт"
    )
    street = models.CharField(
        max_length=225, null=True, blank=True, verbose_name="Улица"
    )
    house = models.CharField(
        max_length=10, verbose_name="Номер дома", null=True, blank=True
    )
    apt = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="Квартира"
    )
    postal_code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Почтовый индекс"
    )

    def __str__(self):
        return f'{self.street}, {self.city}, {self.region}, {self.postal_code}'




class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Всего"
    )
    paid = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_total_price(self):
        self.total_price = sum(
            self.item.quantity * item.product_price_at_order
            for item in self.items.all()
        )

    def __str__(self):
        return f'Order {self.id} - {self.customer}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_price_at_order = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа"
    )

    def __str__(self):  # noqa: D105
        return (
            f"{self.quantity} X {self.product.title} @ "
            f"{self.product_price_at_order}"
        )
