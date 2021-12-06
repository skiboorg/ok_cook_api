# Generated by Django 3.2.9 on 2021-12-06 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='order',
            name='company_address',
            field=models.TextField(blank=True, null=True, verbose_name='Юридический адрес'),
        ),
        migrations.AddField(
            model_name='order',
            name='company_contact',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Контактное лицо'),
        ),
        migrations.AddField(
            model_name='order',
            name='company_inn',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='ИНН'),
        ),
        migrations.AddField(
            model_name='order',
            name='company_kpp',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='КПП'),
        ),
        migrations.AddField(
            model_name='order',
            name='company_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название компании'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Телефон'),
        ),
    ]
