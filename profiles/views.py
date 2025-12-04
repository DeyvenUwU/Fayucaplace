from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from .forms import NewProfileForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signUp(request):
    if request.method == 'GET':
        return render(request, 'signUp.html', {
            'form': NewProfileForm()
        })

    form = NewProfileForm(request.POST)
    if form.is_valid():
        # Crear usuario
        user = form.save()

        # Crear perfil asociado
        Profile.objects.create(
            user=user,
            email=form.cleaned_data['email']
        )

        # Iniciar sesión
        login(request, user)
        return redirect('mainPanel')

    # Si el formulario no es válido, se vuelve a renderizar con errores
    return render(request, 'signUp.html', {
        'form': form,
        'error': 'Por favor corrige los errores del formulario.'
    })
    
def signIn(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })

    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('mainPanel')
    else:
        return render(request, 'login.html', {
            'form': form,
            'error': 'El usuario o la contraseña no son correctos.'
        })

def editProfile(request):
    # Obtener o crear profile si no existe
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('mainPanel')
    else:
        form = EditProfileForm(instance=profile, user=request.user)

    return render(request, 'editProfile.html', {'form': form})

def signOut(request):
    logout(request)
    return redirect('home')