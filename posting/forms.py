<<<<<<< HEAD
<<<<<<< HEAD
from django import forms
from .models import Publicacion, Articulo, Anuncio, Categoria, SubCategoria

class ArticleForm (forms.ModelForm):
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")
    cantidad = forms.IntegerField(label="Cantidad")
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoría",
        required=True
    )
    subCategoria = forms.ModelChoiceField(
        queryset=SubCategoria.objects.none(),
        label="Subcategoría",
        required=True
    )
    condicion = forms.ChoiceField(
        choices=Articulo.CONDICION_ARTICULO,
        label="Condición",
        required=True
    )

    class Meta:
        model = Publicacion
        fields = ['imagen', 'titulo', 'descripcion']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se selecciona una categoría en inicial, cargar sus subcategorías
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subCategoria'].queryset = SubCategoria.objects.filter(categoria_id=categoria_id)
            except (ValueError, TypeError):
                pass
    
    def save(self, usuario, commit=True):
        publicacion = super().save(commit=False)
        publicacion.idUsuario = usuario
        if commit:
            publicacion.save()

        articulo = Articulo(
            idPublicacion=publicacion,
            precio=self.cleaned_data['precio'],
            cantidad=self.cleaned_data['cantidad'],
            categoria=self.cleaned_data['categoria'],
            subCategoria=self.cleaned_data['subCategoria'],
            condicion=self.cleaned_data['condicion']
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


class EditArticleForm(forms.ModelForm):
    precio = forms.DecimalField(max_digits=10, decimal_places=2, label="Precio")
    cantidad = forms.IntegerField(label="Cantidad")
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoría",
        required=True
    )
    subCategoria = forms.ModelChoiceField(
        queryset=SubCategoria.objects.none(),
        label="Subcategoría",
        required=True
    )
    condicion = forms.ChoiceField(
        choices=Articulo.CONDICION_ARTICULO,
        label="Condición",
        required=True
    )
    estado = forms.ChoiceField(
        choices=Publicacion.ESTADO_PUBLICACION,
        label="Estado"
    )

    class Meta:
        model = Publicacion
        fields = ['imagen', 'titulo', 'descripcion', 'estado']
    
    def __init__(self, *args, **kwargs):
        self.articulo_instance = kwargs.pop('articulo_instance', None)
        super().__init__(*args, **kwargs)
        
        # Cargar datos del artículo
        if self.articulo_instance:
            self.fields['precio'].initial = self.articulo_instance.precio
            self.fields['cantidad'].initial = self.articulo_instance.cantidad
            self.fields['categoria'].initial = self.articulo_instance.categoria
            self.fields['condicion'].initial = self.articulo_instance.condicion
            
            # Cargar subcategorías de la categoría
            if self.articulo_instance.categoria:
                self.fields['subCategoria'].queryset = SubCategoria.objects.filter(
                    categoria=self.articulo_instance.categoria
                )
                self.fields['subCategoria'].initial = self.articulo_instance.subCategoria
        
        # Si se selecciona una categoría en inicial, cargar sus subcategorías
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                self.fields['subCategoria'].queryset = SubCategoria.objects.filter(categoria_id=categoria_id)
            except (ValueError, TypeError):
                pass
    
    def save(self, commit=True):
        publicacion = super().save(commit=False)
        if commit:
            publicacion.save()

        # Actualizar artículo
        self.articulo_instance.precio = self.cleaned_data['precio']
        self.articulo_instance.cantidad = self.cleaned_data['cantidad']
        self.articulo_instance.categoria = self.cleaned_data['categoria']
        self.articulo_instance.subCategoria = self.cleaned_data['subCategoria']
        self.articulo_instance.condicion = self.cleaned_data['condicion']
        if commit:
            self.articulo_instance.save()

        return publicacion


class EditAdForm(forms.ModelForm):
    fechaInicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de inicio"
    )
    fechaFin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de fin"
    )
    estado = forms.ChoiceField(
        choices=Publicacion.ESTADO_PUBLICACION,
        label="Estado"
    )

    class Meta:
        model = Publicacion
        fields = ['imagen', 'titulo', 'descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        self.anuncio_instance = kwargs.pop('anuncio_instance', None)
        super().__init__(*args, **kwargs)
        
        # Cargar datos del anuncio
        if self.anuncio_instance:
            self.fields['fechaInicio'].initial = self.anuncio_instance.fechaInicio
            self.fields['fechaFin'].initial = self.anuncio_instance.fechaFin

    def save(self, commit=True):
        publicacion = super().save(commit=False)
        if commit:
            publicacion.save()

        # Actualizar anuncio
        self.anuncio_instance.fechaInicio = self.cleaned_data['fechaInicio']
        self.anuncio_instance.fechaFin = self.cleaned_data['fechaFin']
        if commit:
            self.anuncio_instance.save()

        return publicacion
=======
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
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
=======
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
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
