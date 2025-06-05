from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    picture = models.ImageField(null=True, blank=True)


class Testimonal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=5)
    comment = models.TextField()
