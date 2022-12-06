from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class SCUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('email address', unique=True)
    birthday = models.DateField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', null=True)

    subscribes = models.ManyToManyField("cryptos.Crypto", related_name="sub_cryptos")
    likes = models.ManyToManyField("cryptos.Crypto", related_name="like_cryptos")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
