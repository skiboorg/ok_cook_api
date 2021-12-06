from django.db import models


class MenuType(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=True)
    items_count = models.IntegerField('Кол-во товаров', blank=False, null=True)
    items_gift_count = models.IntegerField('Кол-во товаров в подарок', blank=False, null=True)
    price = models.IntegerField('Цена', blank=False, null=True)

    def __str__(self):
        return f'{self.items_count} блюд {self.items_gift_count} в подарок | Цена {self.price}  '

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = '3. Типы меню'


class Category(models.Model):
    name = models.CharField('Название', max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}  '

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = '1. Категории'


class Item(models.Model):
    name = models.CharField('Название', max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='items', verbose_name='Категория')
    image = models.ImageField('Баннер', upload_to='banner', blank=True, null=True)
    items_added = models.IntegerField('Кол-во товаров', blank=True, default=0, editable=False)
    weigth = models.CharField('Вес', max_length=10, blank=True, null=True)
    calories = models.CharField('Калории', max_length=10, blank=True, null=True)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}  '

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '2. Товары'