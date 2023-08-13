from django.contrib import admin
from .models import CustomUser, JobPost, Application

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(JobPost)
admin.site.register(Application)
