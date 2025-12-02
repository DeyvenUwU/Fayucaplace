from django import forms
from .models import Publicacion, Articulo, Anuncio

class ArticleForm (forms.ModelForm):
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")
    cantidad = forms.IntegerField(label="Cantidad")

    class Meta:
        model = Publicacion
        fields = ['imagen', 'titulo', 'descripcion']
    
    def save(self, usuario, commit=True):
        publicacion = super().save(commit=False)
        publicacion.idUsuario = usuario
        if commit:
            publicacion.save()

        articulo = Articulo(
            idPublicacion=publicacion,
            precio=self.cleaned_data['precio'],
            cantidad=self.cleaned_data['cantidad']
        )
        if commit:
            articulo.save()

        return publicacion

class AdForm(forms.ModelForm):
    fechaInicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de inicio"
    )
    fechaFin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de fin"
    )

    class Meta:
        model = Publicacion
        fields = ['imagen', 'titulo', 'descripcion']

    def save(self, usuario, commit=True):
        publicacion = super().save(commit=False)
        publicacion.idUsuario = usuario
        if commit:
            publicacion.save()

        anuncio = Anuncio(
            idPublicacion=publicacion,
            fechaInicio=self.cleaned_data['fechaInicio'],
            fechaFin=self.cleaned_data['fechaFin']
        )
        if commit:
            anuncio.save()

        return publicacion
