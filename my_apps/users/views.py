from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.


def register_view(request):
    return render(request, 'users/register.html')

def login_view(request):
    return render(request, 'users/login.html')


def logout_view(request):
    return redirect('users:login')


def profile_view(request):
    return render(request, 'users/profile.html')