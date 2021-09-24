from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


STATUS_CHOICES = (
    ('open', 'Открытое'),
    ('closed', 'Нет доступа'),
    ('draft', 'В корзину')
)


class Product(models.Model):
    """Классы, которые наследуются от models.Model являются моделями, то есть
    отвечают за связь с БД через ORM, в БД будет создана таблица с указанными
    полями"""
    title = models.CharField('Заголовок', max_length=255)
    # CharField - VARCHAR(), обязательное свойство max_length
    descriptions = models.TextField('Описание')

    price = models.DecimalField('Цена', max_digits=100, decimal_places=2)
    """choices - жёстко ограниченные варианты выбора, т.е никакие иные значения 
    не принимаются"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='prod', verbose_name='Покупатель')
    """ForeignKey - поле для связи с другой моделью, обязательные свойства: модель,
    on_delete - определяет, что произойдёт с объявлением, если удалить автора из БД"""
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    """DateTimeField - TIMESTAMP in SQL, auto_now_add - время задаётся при добавлении записи,
    auto_now - время задаётся при изменении записи"""
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def str(self):
        return f'Id{self.id}:{self.title}'


class Response(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='отзывы', verbose_name='Продукт')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='отзывы', verbose_name='Покупатель')
    text = models.TextField('Текст')
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,
                              null=True,related_name='my_responses')
    readers = models.ManyToManyField(User, through='UserProductRelation')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def str(self):
        return f'{self.owner} --> {self.user}'


class UserProductRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Great'),
        (3, 'Amazing'),
        (4, 'Good'),
        (5, 'Incredible')
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    product = models.ForeignKey(Response,
                                on_delete=models.CASCADE)
    like = models.ManyToManyField(User,related_name='likes')
    favorite = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField()

    def  __str__(self):
        return f'{self.user}: {self.product}, RATE{self.rate}'

class CartProduct(models.Model):
    """Продукт корзины"""
    owner = models.ForeignKey('Customer',verbose_name='Покупатель',on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart',verbose_name='Cart',on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f'Продукт: {self.content_object.name} (для корзины)'

    def save(self,*args,**kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

        class Meta:
            verbose_name = 'Продукт корзины'
            verbose_name_plural = 'Продукты корзины'

class Cart(models.Model):
    """Корзины"""
    owner = models.ForeignKey('Customer',verbose_name='Покупатель',on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct,blank=True,null=True,related_name='related_cart',verbose_name='Продукты для корзины')
    total_products = models.IntegerField(default=1,verbose_name='общее кол-во товара')
    final_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name  = 'Корзина'
        verbose_name_plural = 'Корзины'


