from django import forms
from .models import Project, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'email', 'profile_picture', 'bio']


class NewProjectForm(forms.ModelForm):
      class Meta:
        model = Project
        exclude = ['user']
image = forms.ImageField()
title = forms.CharField(max_length=40)
country = forms.CharField()
project_link = forms.CharField()
descripton = forms.Textarea()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user   
