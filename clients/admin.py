from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "company", "picture"]
    list_filter = ["name", "title", "company"]


class TestimonalAdmin(admin.ModelAdmin):
    list_display = ["client", "rate"]
    list_filter = ["comment"]
