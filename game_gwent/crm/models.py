from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from game_gwent.validators import validate_and_clean_address

from game_gwent.catalog.models import Product


class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    phone_num = PhoneNumberField(region='RU', verbose_name="Номер телефона")
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # noqa: D105
        return f'{self.last_name} {self.first_name} {self.email}'

    class Meta:  # noqa: D106
        verbose_name = "Покупатель"
        verbose_name_plural = 'Покупатели'


class Address(models.Model):
    region = models.CharField(
        max_length=100, verbose_name="Область"
    )
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
    is_manual = models.BooleanField(default=False)

    def clean(self):
        validate_and_clean_address(self)

    def __str__(self):
        return (
            f'{self.region}, {self.city}, {self.street},'
            f'{self.house}, {self.apt}, {self.postal_code}'
        )

    class Meta:  # noqa: D106
        verbose_name = "Адрес"
        verbose_name_plural = 'Адреса'


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Покупатели'
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Всего"
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Адрес заказа"
    )
    user_comment = models.CharField(
        max_length=225, null=True, blank=True,
        verbose_name="Комментарий к заказу"
    )
    paid = models.BooleanField(default=False, verbose_name="Статус оплаты")
    sent = models.BooleanField(default=False, verbose_name="Статус отправки")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оформления заказа"
    )

    def update_total_price(self):
        self.total_price = sum(
            self.item.quantity * item.product_price_at_order
            for item in self.items.all()
        )

    def __str__(self):
        return f'Order {self.id} - {self.customer}'

    class Meta:  # noqa: D106
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'


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
