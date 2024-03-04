from django.db import models
from django.contrib.auth import get_user_model

from articles.models import Article

User = get_user_model()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.text
