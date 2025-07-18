from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_superuser", "is_staff"]
    list_filter = ["is_superuser", "is_staff"]


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["email", "phone", "address", "company_name", "is_default"]


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


class CompanyStatsAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "number_of_employees",
        "number_of_projects_completed",
        "client_satisfication_rate",
        "number_of_happy_clients",
        "number_of_years_in_business",
        "company_location",
    ]


admin.site.register(CompanyStats, CompanyStatsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Message, MessageAdmin)
