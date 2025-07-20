from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    avatar = models.ImageField(null=True, blank=True)


class Testimonal(models.Model):
    name = models.CharField(max_length=255)
    rate = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    avatar = models.ImageField(null=True, blank=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ServiceFeature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    features = models.ManyToManyField(ServiceFeature)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.title
