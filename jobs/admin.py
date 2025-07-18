from django.contrib import admin

from .models import (
    Job,
    JobApplication,
    JobBenefit,
    JobRequirement,
    JobResponsibility,
    Salary,
)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "description", "type", "posted_at")
    search_fields = ("title", "location", "posted_at")
    list_filter = ("posted_at",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "full_name")
    search_fields = ("job",)
    list_filter = ("applied_date",)

    @admin.action(description="Close Jobs")
    def mark_as_closed(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user("Closed Succesfully")

    actions = [mark_as_closed]


@admin.register(JobRequirement)
class JobRequirementAdmin(admin.ModelAdmin):
    list_display = ("requirement",)
    search_fields = ("requirement",)


@admin.register(JobBenefit)
class JobBenefitAdmin(admin.ModelAdmin):
    list_display = ("benefit",)
    search_fields = ("benefit",)


@admin.register(JobResponsibility)
class JobResponsibilityAdmin(admin.ModelAdmin):
    list_display = ("responsibility",)
    search_fields = ("responsibility",)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("min", "max", "currency")
    search_fields = ("min", "max", "currency")
