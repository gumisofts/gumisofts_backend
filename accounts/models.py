from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Organization(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    years_of_exprience = models.PositiveBigIntegerField(default=5)


class Message(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    is_read = models.BooleanField(default=False)
