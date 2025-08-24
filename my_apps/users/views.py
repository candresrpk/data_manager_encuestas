from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guardar usuario en la BD
            user = form.save()
            
            # Autenticar con los datos limpios del form
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            
            # Iniciar sesión
            if user is not None:
                login(request, user)
                messages.success(request, f'Registro exitoso. Bienvenido/a {user.username}!')
                return redirect('users:profile')
            else:
                messages.error(request, "Error al autenticar el usuario. Contacta al administrador.")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Has iniciado sesión como {username}.')
                return redirect('users:profile')
            else:
                messages.error(request, 'Error al autenticar el usuario. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('users:login')


def profile_view(request):
    return render(request, 'users/profile.html')