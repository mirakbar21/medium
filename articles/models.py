from datetime import datetime
from django.conf import settings

from django.db import models
from django.utils.text import slugify

from django.contrib.auth import get_user_model
from categories.models import Category

class Article(models.Model):
    title = models.CharField(max_length = 100)
    subtitle = models.CharField(max_length = 200, null = True)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    publication_date = models.DateField(auto_now_add = True)
    update_date = models.DateField(auto_now = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = True) #todo: make manytoone instead of onetoone
    slug = models.CharField(default = "", max_length = 100, unique = True)
    applauds = models.PositiveIntegerField(default = 0)
    minutes_to_read = models.PositiveIntegerField(default = 1)
    image = models.ImageField(upload_to='article_images/', blank=True, null = True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
            if self._meta.model.objects.filter(slug=self.slug).exists():
                timestamp = datetime.now().strftime('%H-%M-%S-%d-%m-%Y')
                self.slug = f"{self.slug}-{timestamp}"

        # Вычисление времени чтения
        self.minutes_to_read = max(1, len(self.content.replace(' ', '')) // 250)

        super().save(*args, **kwargs)

class Applaud(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'article')  # Уникальная связь пользователя и статьи

    def save(self, *args, **kwargs):
        if not self.pk and Applaud.objects.filter(user=self.user, article=self.article).count() >= 50:
            return
        super(Applaud, self).save(*args, **kwargs)

