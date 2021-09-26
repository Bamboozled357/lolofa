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
        return f'Id{self.user}:{self.title}'


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
                             related_name='отзывы', verbose_name='Продукт')
    author = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Покупатель')
    text = models.TextField('Текст')
    readers = models.ManyToManyField(User, through='UserProductRelation')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):

        return f'{self.product} --> {self.user}'

        return f'{self.text} --> {self.author}'


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

    def __str__(self):
        return f'{self.user}: {self.product}, RATE{self.rate}'


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cards')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', 'id', )


class ProductLikes(models.Model):
    likeusers = models.ManyToManyField(User)
    likeproduct = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='likeproduct')

