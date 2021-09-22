from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STATUS_CHOICES = (
    ('open', 'открытое'),
    ('closed', 'закрытое'),
    ('draft', 'черновик')
)


class Product(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pubs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    publication = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'коментарии'
        verbose_name_plural = 'коментарии'


