from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Organization(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    company_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    years_of_exprience = models.PositiveBigIntegerField(default=5)
    number_of_projects_completed = models.PositiveBigIntegerField(default=10)
    number_of_happy_clients = models.PositiveBigIntegerField(default=10)
    client_satisfication_rate = models.PositiveBigIntegerField(default=98)
    number_of_years_in_business = models.PositiveBigIntegerField(default=5)
    schedule_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    telegram_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    whatsapp_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    number_of_employees = models.PositiveBigIntegerField(default=10)
    number_of_services = models.PositiveBigIntegerField(default=6)
    is_default = models.BooleanField(default=False)


class Message(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()
    is_read = models.BooleanField(default=False)


# ORM
class CompanyStats(models.Model):
    company_name = models.CharField(max_length=255)
    number_of_employees = models.PositiveBigIntegerField(default=10)
    number_of_projects_completed = models.PositiveBigIntegerField(default=10)
    client_satisfication_rate = models.PositiveBigIntegerField(default=10)
    number_of_happy_clients = models.PositiveBigIntegerField(default=10)
    number_of_years_in_business = models.PositiveBigIntegerField(default=5)
    company_location = models.CharField(max_length=255)
