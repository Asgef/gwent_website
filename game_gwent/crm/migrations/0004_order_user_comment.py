# Generated by Django 5.0.6 on 2024-07-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_alter_address_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_comment',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Комментарий к заказу'),
        ),
    ]
