from .models import Project, Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, NewProjectForm
from .email import send_welcome_email


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
            email = form.cleaned_data['email']
            send_welcome_email(user,email)

            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/login")
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name="django_registration/registration_form.html", context= {'form': form})

def login_user(request):
  if request.method == "POST":
      form = AuthenticationForm(request, data=request.POST)
      if form.is_valid():
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(username=username, password=password)
          if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("index")
          else:
            messages.error(request,"Invalid username or password.")
      else:
          messages.error(request,"Invalid username or password.")
  form = AuthenticationForm()

  return render(request=request, template_name="django_registration/login.html", context={"form":form})


  





