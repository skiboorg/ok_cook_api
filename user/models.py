from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from .services import create_random_string,updateRefferals
from cart.models import Cart

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class PaymentMethod(models.Model):
    label = models.CharField('Название способа оплаты', max_length=50, blank=True, null=True)



class User(AbstractUser):
    username = None
    firstname = None
    lastname = None
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    city = models.CharField('Город', max_length=50, blank=True, null=True)
    address = models.TextField('Адрес доставки', blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    own_ref_code = models.CharField('Собственный реф код', max_length=50, blank=True, null=True)
    used_ref_code = models.CharField('Использованный реф код', max_length=50, blank=True, null=True)
    balance = models.DecimalField('Баланс', decimal_places=2, max_digits=6, blank=True, default=0)
    ref_bonuses = models.DecimalField('Реф бонусы', decimal_places=2, max_digits=6, blank=True, default=0)
    total_spend = models.DecimalField('Всего потрачено', decimal_places=2, max_digits=6, blank=True, default=0)

    is_company = models.BooleanField('Это юр. лицо', default=False)
    is_default_reffer = models.BooleanField('По умолчанию', default=False)

    company_name = models.CharField('Название компании', max_length=150, blank=True, null=True)
    company_address = models.TextField('Юридический адрес', blank=True, null=True)
    company_inn = models.CharField('ИНН', max_length=20, blank=True, null=True)
    company_kpp = models.CharField('КПП', max_length=20, blank=True, null=True)
    company_contact = models.CharField('Контактное лицо', max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.fio if self.fio else ""} {self.phone if self.phone else ""} {self.email} '

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '1. Пользователи'


class UserRefferalFirstLine(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             verbose_name='Пользователь',
                             related_name='first_line_refferals',
                             db_index=True
                             )
    users = models.ManyToManyField(User,
                             blank=True,
                             verbose_name='Рефералы',
                             )

    def __str__(self):
        return f'Первая линия пользователя {self.user.fio} | {self.user.email}'

    class Meta:
        verbose_name = 'Первая линия'
        verbose_name_plural = '2. Первые линии'


class UserRefferalSecondLine(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             verbose_name='Пользователь',
                             related_name='second_line_refferals',
                             db_index=True
                             )
    users = models.ManyToManyField(User,
                             blank=True,
                             verbose_name='Рефералы',
                             )

    def __str__(self):
        return f'Вторая линия пользователя {self.user.email}'

    class Meta:
        verbose_name = 'Вторая линия'
        verbose_name_plural = '3. Вторые линии'


class UserRefferalThirdLine(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             verbose_name='Пользователь',
                             related_name='third_line_refferals',
                             db_index=True
                             )
    users = models.ManyToManyField(User,
                             blank=True,
                             verbose_name='Рефералы',
                             )

    def __str__(self):
        return f'Третья линия пользователя {self.user.email}'

    class Meta:
        verbose_name = 'Третья линия'
        verbose_name_plural = '4. Третие линии'

def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        # Cart.objects.create(user=instance)
        instance.own_ref_code = 'OK-' + create_random_string(digits=False,num=6).upper()
        instance.save(update_fields=['own_ref_code'])
        updateRefferals()




post_save.connect(user_post_save, sender=User)