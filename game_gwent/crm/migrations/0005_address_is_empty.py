# Generated by Django 5.0.6 on 2024-07-10 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_order_user_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_empty',
            field=models.BooleanField(default=False),
        ),
    ]
