from django.contrib import admin

from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "company", "avatar"]
    list_filter = ["name", "title", "company"]
    search_fields = ["name", "title", "company"]


class TestimonalAdmin(admin.ModelAdmin):
    list_display = ["name", "rate", "position", "is_active"]
    search_fields = ["name", "position"]

    def activate_testimonal(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_testimonal(self, request, queryset):
        queryset.update(is_active=False)

    actions = [activate_testimonal, deactivate_testimonal]


class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "category"]
    search_fields = ["title", "category"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Testimonal, TestimonalAdmin)
admin.site.register(ServiceFeature, ServiceFeatureAdmin)
admin.site.register(Service, ServiceAdmin)
