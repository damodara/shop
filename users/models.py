from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=11, unique=True, verbose_name='Телефон', null=True, blank=True)
    country = models.TextField(verbose_name="Страна", null=True, blank=True, max_length=50)
    avatar = models.ImageField(upload_to='users/avatars', null=True, blank=True, verbose_name="Аватар")
    token = models.CharField(max_length=100, null=True, blank=True, verbose_name="Token")
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


    def __str__(self):
        return self.email

