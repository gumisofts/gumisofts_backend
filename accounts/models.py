from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Organization(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    years_of_exprience = models.PositiveBigIntegerField(default=5)


class Mission(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()


class Message(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
