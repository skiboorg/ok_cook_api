from django.db import models


class Cart(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True,related_name='cart')
    session_id = models.CharField('Сессия', max_length=50, blank=True, null=True)
    price = models.IntegerField(default=0)
    items_count = models.IntegerField(default=0)
    # def save(self, *args, **kwargs):
    #
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f'Корзина пользователя {self.user.email}'
        else:
            return f'Корзина гостя {self.id} '

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    item = models.ForeignKey('data.Item', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=0)



class CartComplect(models.Model):
    uid = models.CharField(max_length=100,blank=True,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='complects')
    complect = models.ForeignKey('data.Complect', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    # def save(self, *args, **kwargs):
    #     price = 0
    #     for item in self.items:
    #     self.price = self.amount * self.item.price
    #     super().save(*args, **kwargs)


class CartComplectItem(models.Model):
    cart_complect = models.ForeignKey(CartComplect, on_delete=models.CASCADE, blank=True, null=True,related_name='items')
    item = models.ForeignKey('data.Item', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=1)
    price = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        self.price = self.amount * self.item.price
        super().save(*args, **kwargs)

