
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.categoria.nombre} - {self.nombre}'

class Publicacion(models.Model):
    ESTADO_PUBLICACION = [
        ('ACTIVA', 'Activa'),
        ('PAUSADA', 'Pausada'),
    ]

    titulo = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='publicaciones/fotos/', blank=True, null=True)
    descripcion = models.TextField()
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PUBLICACION, default='ACTIVA')

    def __str__(self):
        return f"{self.titulo} - by {self.idUsuario.username}"


class Articulo(models.Model):
    CONDICION_ARTICULO = [
        ('NUEVO', 'Nuevo'),
        ('USADO', 'Usado'),
    ]

    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='articulo')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    subCategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True, blank=True)
    condicion = models.CharField(max_length=10, choices=CONDICION_ARTICULO, default='USADO')


class Anuncio(models.Model):
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='anuncio')
    fechaInicio = models.DateField()
    fechaFin = models.DateField()


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.categoria.nombre} - {self.nombre}'

class Publicacion(models.Model):
    ESTADO_PUBLICACION = [
        ('ACTIVA', 'Activa'),
        ('PAUSADA', 'Pausada'),
    ]

    titulo = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='publicaciones/fotos/', blank=True, null=True)
    descripcion = models.TextField()
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PUBLICACION, default='ACTIVA')
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - by {self.idUsuario.username}"


class Articulo(models.Model):
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='articulo')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()


class Anuncio(models.Model):
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='anuncio')
    fechaInicio = models.DateField()
    fechaFin = models.DateField()


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.categoria.nombre} - {self.nombre}'

class Publicacion(models.Model):
    ESTADO_PUBLICACION = [
        ('ACTIVA', 'Activa'),
        ('PAUSADA', 'Pausada'),
    ]

    titulo = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='publicaciones/fotos/', blank=True, null=True)
    descripcion = models.TextField()
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PUBLICACION, default='ACTIVA')
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - by {self.idUsuario.username}"


class Articulo(models.Model):
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='articulo')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()


class Anuncio(models.Model):
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='anuncio')
    fechaInicio = models.DateField()
    fechaFin = models.DateField()