from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=11, unique=True, verbose_name='Телефон', null=True, blank=True)
    country = models.TextField(verbose_name="Страна", null=True, blank=True, max_length=50)
    avatar =models.ImageField(upload_to='users/avatars', null=True, blank=True, verbose_name="Аватар")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


    def __str__(self):
        return self.email

