from django.contrib import admin

from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "company", "avatar"]
    list_filter = ["name", "title", "company"]
    search_fields = ["name", "title", "company"]


class TestimonalAdmin(admin.ModelAdmin):
    list_display = ["name", "rate", "position"]
    search_fields = ["name", "position"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Testimonal, TestimonalAdmin)
