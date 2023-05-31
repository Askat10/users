# Create your models here.
""" 
1. Описать модель - models.py
2. Добавить в админку - admin.py
3. Отсериализовать - serializers.py
4. Отобразить - views.py
5. Привязать путь/ссылку - urls.py
"""

from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class StatusChoices(models.TextChoices):
    processing = 'processing'
    published = 'published'

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField('Tag', related_name='articles')
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default='processing')
    image = models.ImageField(upload_to='articles', )


    
    def __str__(self) -> str:
        return self.title
    

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

        


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

