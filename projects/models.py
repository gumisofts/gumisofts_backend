from django.db import models


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField()
    descriptions = models.TextField()
    status = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
