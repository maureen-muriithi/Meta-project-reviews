from .models import Project, Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, NewProjectForm, UpdateProfileForm
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



@login_required(login_url='/accounts/login/')
def profile(request):
    user = request.user
    # projects = Project.objects.filter(user=request.user).all(),
    args = {
        'user': user,
        'projects': Project.objects.filter(user=request.user).all()
    }
    return render(request, 'projects/profile.html', args)


@login_required(login_url='/accounts/login/')
def display_projects(request):
    projects = Project.objects.all()

    args = {
        "projects": projects,
    }
    return render(request, 'projects/projects.html', args) 


@login_required(login_url='/accounts/login/')
def single_project(request, project_id):
    projects = Project.objects.filter(id=project_id).all()

    args = {
        "projects": projects,
    }
    return render(request, 'projects/single_project.html', args) 


@login_required(login_url='/accounts/login/')
def search_project(request):
    projects = Project.objects.all()
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        projects = Project.search_project_name(search_term)
        message = f'{search_term}'

        args = {
        "projects": projects,
        "message": message
    }

        return render(request, 'search_project.html', args)
    else:
        message = 'Ooops! We currently do not have such a project'
        return render(request, 'projects/search_project.html', {'message': message})


@login_required(login_url='/accounts/login/')
def submit_project(request):
    user = request.user
    if request.method == "POST":
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = user
            post.save()
            return redirect("index")
    else:
        form = NewProjectForm()
        args = {
          "form": form,  
        }

    return render(request, "projects/new_project.html", args)


@login_required(login_url='/accounts/login/')
def not_found(request):
    message = 'Sorry. We have nothing at the moment. Please check again later'
    return render(request, 'projects/notfound.html', {"message":message})







  





