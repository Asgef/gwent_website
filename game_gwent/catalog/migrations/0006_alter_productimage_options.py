# Generated by Django 5.0.6 on 2024-07-04 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_productimage_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'Галереи для игры', 'verbose_name_plural': 'Галереи'},
        ),
    ]