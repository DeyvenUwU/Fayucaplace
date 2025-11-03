from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='articulo')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()


class Anuncio(models.Model):
    idPublicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='anuncio')
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

