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

    def __str__(self):
        return self.name


# {
#       id: 2,
#       name: "Michael Chen",
#       position: "CTO, InnovateLab",
#       rating: 5,
#       comment: "Outstanding work on our mobile application. The development process was smooth, and the final product was exactly what we envisioned. Highly recommended for any software development needs.",
#       avatar: "/assets/avatar2.jpg"
#     },
