from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>', views.update_profile, name='update_profile'),
    path('projects/', views.display_projects, name='projects'),
    path("projects/<int:project_id>/", views.single_project, name='single_project'),
    path('search/', views.search_project, name='search'),
    path('newproject/', views.submit_project, name="submit_project"),
    path('notfound/', views.not_found, name='not_found'),
    path('api/profiles/', views.ProfileViewItems.as_view()),
    path('api/projects/', views.ProjectViewItems.as_view())

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)