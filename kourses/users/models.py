from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите почту')
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Телефон', help_text='Укажите телефон')
