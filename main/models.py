from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = (
    ('open', 'Открытое'),
    ('closed', 'Нет доступа'),
    ('draft', 'В корзину')
)


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField('Название', max_length=200)
    descriptions = models.TextField('Описание')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES)
    price = models.DecimalField('Цена', max_digits=100, decimal_places=2)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='prod', verbose_name='Покупатель')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Response(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='comments', verbose_name='Продукт')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Покупатель')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.product} --> {self.user}'

