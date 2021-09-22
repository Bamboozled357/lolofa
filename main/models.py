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

    def __str__(self):
        return self.title


class Response(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='отзывы', verbose_name='Продукт')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='отзывы', verbose_name='Покупатель')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.product} --> {self.user}'

