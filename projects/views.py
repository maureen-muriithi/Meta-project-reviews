from .models import Project, Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, NewProjectForm

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


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
          user = form.save()
          login(request, user)
          messages.success(request, "Registration successful." )
        return redirect("/login")
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name="django_registration/registration_form.html", context= {'form': form})

