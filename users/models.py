from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profile_photos/', default = 'profile_photos/account_3033143.png', blank=True)
    following = models.ManyToManyField(
        'self',
        related_name = 'followers',
        symmetrical = False,
        blank = True
    )