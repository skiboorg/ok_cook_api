# Generated by Django 3.2.9 on 2021-12-16 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cartcomplect_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartcomplect',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartcomplectitem',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
