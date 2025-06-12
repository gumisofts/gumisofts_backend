from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_superuser", "is_staff"]
    list_filter = ["is_superuser", "is_staff"]


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["email", "phone", "address"]


@admin.action(
    description="Marking messages as read",
)
def mark_messages_as_read(self, request, queryset):
    queryset.update(is_read=True)

    self.message_user(request, "Successfully Marked")


class MessageAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "content", "is_read"]
    list_filter = ["is_read"]

    actions = [mark_messages_as_read]


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Message, MessageAdmin)
