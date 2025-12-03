<<<<<<< HEAD
<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class NewProfileForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Elige otro.")
        return username

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre de usuario'
    )
    email = forms.EmailField(
        required=False,
        label='Correo electrónico',
        disabled=True
    )
    phoneNumber = forms.CharField(
        max_length=10,
        required=False,
        label='Número de teléfono'
    )

    class Meta:
        model = Profile
        fields = ['image', 'username', 'email', 'phoneNumber']
        labels = {
            'image': 'Foto de perfil',
            'phoneNumber': 'Número de teléfono',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['email'].disabled = True

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        # No actualizamos el email ya que está deshabilitado

        if commit:
            user.save()
            profile.save()
        return profile
=======
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class NewProfileForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Elige otro.")
        return username

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre de usuario'
    )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico'
    )

    class Meta:
        model = Profile
        fields = ['image', 'username', 'email']
        labels = {
            'image': 'Foto de perfil',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()
        return profile
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
=======
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class NewProfileForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Elige otro.")
        return username

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre de usuario'
    )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico'
    )

    class Meta:
        model = Profile
        fields = ['image', 'username', 'email']
        labels = {
            'image': 'Foto de perfil',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()
        return profile
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
