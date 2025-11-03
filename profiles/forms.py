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
    name = forms.CharField(
        max_length=150,
        required=False,
        label='Nombre completo',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # visible pero no editable
    )
    email = forms.EmailField(
        required=False,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'readonly': 'readonly'})  # visible pero no editable
    )

    class Meta:
        model = Profile
        fields = ['photo', 'username', 'name', 'phone', 'email']
        labels = {
            'photo': 'Foto de perfil',
            'phone': 'Teléfono',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # recibimos el usuario actual
        super().__init__(*args, **kwargs)

        if user:
            # Prellenar datos desde User y Profile
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['name'].initial = self.instance.name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Actualizar el username y el phone
        user = profile.user
        user.username = self.cleaned_data['username']
        profile.phone = self.cleaned_data['phone']

        if commit:
            user.save()
            profile.save()
        return profile
