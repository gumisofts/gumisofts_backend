from django.db import models
from django.utils import timezone


class Technology(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create your models here.
class Project(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now=True)
    completed_percentage = models.IntegerField(default=80)
    is_featured = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Technology, related_name="projects")
    demo_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
