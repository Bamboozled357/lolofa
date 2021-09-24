from pyexpat import model

from django.conf import settings
from django.db import models
from django.utils import timezone

from main.models import Cart, Product


class Order(models.Model):
    """Заказ пользователя"""


    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказв обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ получен')

    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF,'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey('Customer',verbose_name='Покупатель',
                                 related_name='orders',on_delete=models.CASCADE)
    name = models.CharField(max_length=255,verbose_name='Имя')
    last_name = models.CharField(max_length=255,verbose_name='Фамилия')
    phone = models.CharField(max_length=20,verbose_name='Номер телефона')
    cart = models.ForeignKey(Cart,verbose_name='корзина',on_delete=models.CASCADE)
    address = models.CharField(max_length=1024,verbose_name='Адрес',null=True,blank=True)
    status = models.CharField(max_length=100,verbose_name='Статус заказа',choices=STATUS_CHOICES,
                              default=STATUS_NEW)
    buying_type = models.CharField(max_length=100,verbose_name='Тип заказа',choices=BUYING_TYPE_CHOICES)
    feedback = models.TextField(verbose_name='Комментарий к заказу',null=True,blank=True)
    created_at = models.DateField(verbose_name='Дата создания заказа',auto_now=True)
    order_date = models.DateField(verbose_name='Дата получения заказа',default=timezone.now)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Customer(models.Model):
    """Покупатель"""
    user = models.OneToOneField(settings.AUTH_MODEL_USER, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True,verbose_name='Активный')
    customer_orders = models.ManyToManyField(Order,blank=True,related_name='related_customer')
    wishlist = models.ManyToManyField(Product,blank=True,verbose_name='Список ожидаемого')
    phone = models.CharField(max_length=20,verbose_name='Номер')
    address = models.TextField(null=True,blank=True,verbose_name='Адрес')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

class Notification(models.Model):
    """Уведомления"""

    recipient = models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='Получатель')
    text = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Увеломления для {self.recipient.user.username} | id={self.id}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведоиления'