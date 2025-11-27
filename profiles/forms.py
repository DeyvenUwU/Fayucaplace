from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class NewProfileForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_ permitidos.',
            'password1': 'Tu contraseña debe contener al menos 8 caracteres y no puede ser completamente numérica.',
            'password2': 'Ingresa la misma contraseña para verificación.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de error en español
        self.fields['password1'].help_text = (
            '<ul>'
            '<li>Tu contraseña debe contener al menos 8 caracteres.</li>'
            '<li>Tu contraseña no puede ser completamente numérica.</li>'
            '<li>Tu contraseña no puede ser demasiado común.</li>'
            '<li>Tu contraseña no puede ser muy similar a tu información personal.</li>'
            '</ul>'
        )
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para verificación.'
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_ permitidos.'
        
        # Personalizar mensajes de error de validación
        self.fields['username'].error_messages = {
            'required': 'Este campo es obligatorio.',
            'invalid': 'Ingresa un nombre de usuario válido.',
            'unique': 'Este nombre de usuario ya está en uso.',
        }
        self.fields['email'].error_messages = {
            'required': 'Este campo es obligatorio.',
            'invalid': 'Ingresa un correo electrónico válido.',
        }
        self.fields['password1'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

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
