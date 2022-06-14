from .models import Project, Profile, Review
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
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import ProfileSerializer, ProjectSerializer
from .permissions import IsAdminOrReadOnly



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

  return render(request=request, template_name="registration/login.html", context={"form":form})



@login_required(login_url='/accounts/login/')
def profile(request):
    user = request.user
    profile = Profile.objects.filter(user_id=user.id).first()
    project = Project.objects.filter(user_id=user.id)
    args = {
        'user': user,
        'project': project,
        'profile' : profile,

    }
    return render(request, 'projects/profile.html', args)

@login_required(login_url='/accounts/login/')
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  

                profile = form.save(commit=False)
                profile.save()
                return redirect('profile') 

    args = {"form":form}
    return render(request, 'projects/update_profile.html', args)   


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
    reviews = Review.objects.filter(project_id = project_id).all()

    args = {
        "projects": projects,
        "reviews": reviews,
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
        return render(request, 'projects/search_project.html', args)
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
def review_project(request,id):
    if request.method == 'POST':
        project = Project.objects.get(id=id)
        current_user = request.user

        design = request.POST['design']
        content = request.POST['content']
        usability= request.POST['usability']

        Review.objects.create(
            project=project,
            user=current_user,
            design=design,
            usability=usability,
            content=content,
            average_score=round((float(design)+float(usability)+float(content))/3,2),
        )

        
        return render(request,'projects/single_project.html',{"project":project})

    else:
        project = Project.objects.get(id=id)

        return render(request,'projects/single_project.html',{"project":project})


@login_required(login_url='/accounts/login/')
def not_found(request):
    message = 'Sorry. We have nothing at the moment. Please check again later'
    return render(request, 'projects/notfound.html', {"message":message})

class ProjectViewItems(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProfileViewItems(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)







  





