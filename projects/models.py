from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    '''
    This is a class model to get and display projects
    '''
    title = models.CharField(max_length=140)
    user = models.ForeignKey(User, null=True, blank=True, related_name='projects', on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'projects/', default='')
    description = models.TextField()
    country = models.CharField(max_length=140)
    project_link = models.URLField(max_length=2048)

    def __str__(self):
        return self.title
    
    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()
        
    @classmethod
    def search_project(cls, title):
        return cls.objects.filter(title__icontains=title).all()
   
    @classmethod
    def all_projects(cls):
        return cls.objects.all()   


class Profile(models.Model):
    '''
    This is a class model to get and display a user's profile

    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' )
    name = models.CharField(max_length=140)
    bio = models.TextField(null=True, default="This is my fine Bio", blank=True)
    profile_picture = models.ImageField(upload_to = 'images/', default='')
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save( *args, **kwargs)

class Review(models.Model):
    '''
    This a class model to enable the user to review and rate projects
    '''
    design = models.IntegerField(default=0, blank=True)
    content = models.IntegerField(default=0, blank=True)
    usability = models.IntegerField(default=0, blank=True)
    average_score = models.IntegerField(default=0, blank=True)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.title} Rating'

    def save_reviews(self):
        self.save()
    
    def delete_reviews(self):
        self.delete()

    @classmethod
    def get_reviews(cls, id):
        reviews = Review.objects.filter(project_id=id).all()
        return reviews




