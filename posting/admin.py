from django.contrib import admin
from .models import Publicacion, Articulo, Anuncio

# Register your models here.
admin.site.register(Publicacion)
admin.site.register(Articulo)
admin.site.register(Anuncio)