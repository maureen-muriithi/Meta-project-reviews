from .models import Project, Profile
from django.shortcuts import render
from django.contrib.auth.models import User
import datetime as dt

# Create your views here.

def index(request):
    date = dt.date.today()
    projects = Project.objects.all()
    users = User.objects.exclude(id=request.user.id)

    args = {
        "date": date, 
        "projects": projects,
        "users": users,
    }

    return render(request, 'projects/index.html', args)


