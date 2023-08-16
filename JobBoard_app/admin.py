from django.contrib import admin
from .models import JobPost

class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'contact_email']
    search_fields = ['title', 'description']
    list_filter = ['title']

admin.site.register(JobPost, JobPostAdmin)
