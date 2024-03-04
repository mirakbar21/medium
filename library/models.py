from django.db import models
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()

class ReadingList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    articles = models.ManyToManyField(Article, blank=True)

    def __str__(self):
        return self.name
