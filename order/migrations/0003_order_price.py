# Generated by Django 3.2.9 on 2021-12-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Стоимость заказа'),
        ),
    ]
