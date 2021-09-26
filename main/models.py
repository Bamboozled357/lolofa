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

    def __str__(self):
        return f'Id{self.user}:{self.title}'


class Response(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='отзывы', verbose_name='Продукт')
    author = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='отзывы', verbose_name='Покупатель')
    text = models.TextField('Текст')
    readers = models.ManyToManyField(User, through='UserProductRelation')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
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

    def  __str__(self):
        return f'{self.user}: {self.product}, RATE{self.rate}'


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cards')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created','id' )


class ProductLikes(models.Model):
    likeusers = models.ManyToManyField(User)
    likeproduct = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, related_name='likeproduct')



