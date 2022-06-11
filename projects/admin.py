from django.contrib import admin
from .models import Profile, Project

# Register your models here.
admin.site.site_header = 'Meta-Projects-Reviews - Administration'
admin.site.register(Profile)
admin.site.register(Project)
