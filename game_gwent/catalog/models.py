from django.db import models


class Product(models.Model):  # noqa: D101

    GENRE_CHOICES = [
        ('strategy', 'Стратегия'),
        ('adventure', 'Приключения'),
        ('puzzle', 'Головоломка'),
        ('family', 'Семейная'),
        ('party', 'Партийная'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    stock = models.PositiveIntegerField(verbose_name="Количество на складе")
    created_at = models.DateTimeField(verbose_name="Дата добавления")

    label = models.CharField(
        max_length=150, unique=False, blank=False, verbose_name="Тег"
    )
    genre = models.CharField(
        max_length=50, choices=GENRE_CHOICES, verbose_name="Жанр"
    )

    publisher = models.CharField(max_length=255, verbose_name="Издатель")
    age = models.PositiveIntegerField(verbose_name="Рекомендуемый возраст")

    image = models.ImageField(
        upload_to='board_games/', blank=True,
        null=True, verbose_name="Изображение"
    )

    def __str__(self):  # noqa: D105
        return self.title

    class Meta:  # noqa: D106
        verbose_name = "Настольная игра"
        verbose_name_plural = 'Настольные игры'
        ordering = ['title']