from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=140)
    user = models.ForeignKey(User, )
    image = models.ImageField(default='')
    description = models.TextField()
    country = models.CharField(max_length=140)
    project_link = models.CharField(max_length=2048)

    def __str__(self):
        return self.title()

