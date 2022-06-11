from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    '''
    This is a class model to get and display projects
    '''
    title = models.CharField(max_length=140)
    user = models.ForeignKey(User, )
    image = models.ImageField(upload_to = 'projects/', default='')
    description = models.TextField()
    country = models.CharField(max_length=140)
    project_link = models.CharField(max_length=2048)

    def __str__(self):
        return self.title

class Profile(models.Model):
    '''
    This is a class model to get and display a user's profile

    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' )
    name = models.CharField(max_length=140)
    bio = models.TextField()
    image = models.ImageField(upload_to = 'images/', default='')
    phone = models.IntegerField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f'{self.user.username} Profile'



