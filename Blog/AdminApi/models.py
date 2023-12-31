from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name= models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255,unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.username
# Create your models here.
