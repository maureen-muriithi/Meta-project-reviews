from django.test import TestCase
from .models import Profile, Project, Review
from django.contrib.auth.models import User


# Create your tests here.
class TestProfile(TestCase):
    '''
    Test case for the profile model.
    '''
    def setUp(self):
        self.user = User(id=1, username='Moh', password='mypassword')
        self.user.save()

        self.profile = Profile(
            name = "Maureen Muriithi",
            profile_picture = "default.jpg",
            bio = "This is my amazing bio",
            email = "moh2wanja@gmail.com",
            phone = "0713925352",
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()


class ProjectTest(TestCase):
    '''
    Test case for the project model
    '''
    def setUp(self):
        self.user = User.objects.create(id=1, username='Moh', password='mypassword')
        self.project = Project.objects.create(
            id=1, 
            title='My project', 
            image='https://ucarecdn.com/0ccf61ff-508e-46c6-b713-db51daa6626e', 
            description='This is my amazing project',
            country = 'Kenya',
            user=self.user, 
            project_link='https://project/link',
            )

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_project(self):
        self.project.save_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)

    def test_get_all_projects(self):
        self.project.save()
        projects = Project.all_projects()
        self.assertTrue(len(projects) > 0)

    def test_search_project(self):
        self.project.save()
        project = Project.search_project('test')
        self.assertTrue(len(project) > 0)

    def test_delete_project(self):
        self.project.delete_project()
        project = Project.search_project('test')
        self.assertTrue(len(project) < 1)
