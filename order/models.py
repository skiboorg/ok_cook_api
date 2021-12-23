from django.db import models
from django.utils.safestring import mark_safe


class Order(models.Model):
    code = models.CharField('Код заказа', max_length=10, blank=True, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True,verbose_name='Пользователь')
    city = models.CharField('Город', max_length=50, blank=True, null=True)
    delivery_time = models.CharField('Время доставки', max_length=50, blank=True, null=True)
    address = models.TextField('Адрес доставки', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    company_name = models.CharField('Название компании', max_length=150, blank=True, null=True)
    company_address = models.TextField('Юридический адрес', blank=True, null=True)
    company_inn = models.CharField('ИНН', max_length=20, blank=True, null=True)
    company_kpp = models.CharField('КПП', max_length=20, blank=True, null=True)
    company_contact = models.CharField('Контактное лицо', max_length=100, blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    is_pay = models.BooleanField('Оплачен', default=False)
    is_done = models.BooleanField('Обработан', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField('Стоимость заказа', default=0)
    delivery_price = models.IntegerField('Стоимость доставки', default=0)

    def __str__(self):
        return f'Код заказа {self.code} | ID{self.id} | Пользователь {self.user.email}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='order_items')
    item = models.ForeignKey('data.Item', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Товар в заказе')
    amount = models.IntegerField('Количество',default=0)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.item.image.url))
    image_tag.short_description = 'Изображение товара'



