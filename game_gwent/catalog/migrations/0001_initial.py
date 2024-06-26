# Generated by Django 5.0.6 on 2024-06-14 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('stock', models.PositiveIntegerField(verbose_name='Количество на складе')),
                ('created_at', models.DateTimeField(verbose_name='Дата добавления')),
                ('label', models.CharField(max_length=150, verbose_name='Тег')),
                ('genre', models.CharField(choices=[('strategy', 'Стратегия'), ('adventure', 'Приключения'), ('puzzle', 'Головоломка'), ('family', 'Семейная'), ('party', 'Партийная'), ('other', 'Другое')], max_length=50, verbose_name='Жанр')),
                ('publisher', models.CharField(max_length=255, verbose_name='Издатель')),
                ('age', models.PositiveIntegerField(verbose_name='Рекомендуемый возраст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='board_games/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Настольная игра',
                'verbose_name_plural': 'Настольные игры',
                'ordering': ['title'],
            },
        ),
    ]
