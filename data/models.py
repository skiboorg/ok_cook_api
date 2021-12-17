from django.db import models
from django.utils.safestring import mark_safe


class Complect(models.Model):
    name = models.CharField('Название', max_length=100, blank=False, null=True)
    items_count = models.IntegerField('Обязательное кол-во товаров', blank=False, null=True)
    show_items_amount = models.BooleanField('Можно добавить более одного товара', default=False)
    is_unlimited = models.BooleanField('Без ограничений по количеству', default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рацион'
        verbose_name_plural = '3. Рационы'


class Category(models.Model):
    name = models.CharField('Название', max_length=100, blank=True, null=True)
    must_check_one_item = models.BooleanField('Должно быть выбрано 1 блюдо из этой категории', default=False)

    def __str__(self):
        return f'{self.name}  '

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = '1. Категории'


class Item(models.Model):
    name = models.CharField('Название', max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='items', verbose_name='Категория')
    image = models.ImageField('Изображение товара', upload_to='items', blank=True, null=True)
    items_added = models.IntegerField('Кол-во товаров', blank=True, default=0, editable=False)
    weigth = models.CharField('Вес', max_length=10, blank=True, null=True)
    calories = models.CharField('Калории', max_length=10, blank=True, null=True)
    is_selected = models.BooleanField(default=False,editable=False)
    price = models.IntegerField('Цена', default=300)

    def __str__(self):
        return f'{self.name}  '

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = '2. Товары'

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))


    image_tag.short_description = 'Изображение товара'