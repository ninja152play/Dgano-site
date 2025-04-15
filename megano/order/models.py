from django.db import models
from product.models import Product
from user.models import Profile

# Create your models here.
class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    fullName = models.CharField(max_length=255, verbose_name='Имя', null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', null=True, blank=True)
    deliveryType = models.CharField(max_length=255, verbose_name='Доставка', null=True, blank=True, default='ordinary')
    paymentType = models.CharField(max_length=255, verbose_name='Оплата', null=True, blank=True, default='online')
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', null=True, blank=True)
    status = models.CharField(max_length=100, default=False, verbose_name='Статус')
    city = models.CharField(max_length=255, verbose_name='Город', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    products = models.ManyToManyField(Product, verbose_name='Товары')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Payment(models.Model):
    namber = models.CharField(max_length=255, verbose_name='Номер карты')
    name = models.CharField(max_length=255, verbose_name='Имя')
    month = models.CharField(max_length=255, verbose_name='Месяц')
    year = models.CharField(max_length=255, verbose_name='Год')
    code = models.CharField(max_length=255, verbose_name='Код')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', null=True, blank=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'


class OrderProductCount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Количество товаров в заказе'



