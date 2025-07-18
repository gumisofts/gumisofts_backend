from django.contrib import admin

from projects.models import Project, Technology

# Register your models here.


@admin.action(description="Mark as completed")
def mark_as_completed(self, request, queryset):
    queryset.update(is_completed=True)

    self.message_user("Updated successfully")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "image", "description", "status", "is_completed"]
    list_filter = ["status", "is_completed"]

    actions = [mark_as_completed]


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology, TechnologyAdmin)
