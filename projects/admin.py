from django.contrib import admin
from .models import Profile, Project, Review

# Register your models here.
admin.site.site_header = 'Meta-Projects-Reviews - Administration'
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Review)

