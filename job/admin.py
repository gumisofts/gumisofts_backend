from django.contrib import admin
from .models import Job,JobApplication
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'description','type','posted_date')  
    search_fields = ('title', 'location','post_date')  
    list_filter = ('posted_date',)  
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display=('job',
                  'full_name')
    search_fields=('job',)
    list_filter=('applied_date',)