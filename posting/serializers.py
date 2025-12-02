from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import Publicacion, Articulo, Anuncio, Categoria, SubCategoria

class SubCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoria
        fields = ['id', 'nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    subcategorias = SubCategoriaSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'subcategorias']

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ['precio', 'cantidad']

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = ['fechaInicio', 'fechaFin']

class PublicacionSerializer(serializers.ModelSerializer):
    """
    Serializer de publicaciones que soporta dos modos de creación:
    1. Modo anidado (compatibilidad existente): campos articulo_data / anuncio_data (JSON) enviados via fetch con application/json.
    2. Modo plano (nuevo): enviar campos simples precio, cantidad, fechaInicio, fechaFin junto con la imagen usando multipart/form-data.

    Esto permite subir la imagen de la publicación sin tener que serializar objetos anidados en JSON.
    """
    articulo = serializers.SerializerMethodField()
    anuncio = serializers.SerializerMethodField()
    idUsuario = serializers.ReadOnlyField(source='idUsuario.username')
    subcategoria_nombre = serializers.StringRelatedField(source='subcategoria', read_only=True)
    subcategoria = serializers.PrimaryKeyRelatedField(
        queryset=SubCategoria.objects.all(), write_only=True, required=False, allow_null=True
    )

    # Modo anidado (existente)
    articulo_data = ArticuloSerializer(write_only=True, required=False)
    anuncio_data = AnuncioSerializer(write_only=True, required=False)

    # Modo plano (nuevo)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, write_only=True)
    cantidad = serializers.IntegerField(required=False, write_only=True)
    fechaInicio = serializers.DateField(required=False, write_only=True)
    fechaFin = serializers.DateField(required=False, write_only=True)

    class Meta:
        model = Publicacion
        fields = [
            'id', 'titulo', 'imagen', 'descripcion', 'idUsuario', 'fechaPublicacion', 'estado',
            'subcategoria', 'subcategoria_nombre', 'articulo', 'anuncio',
            'articulo_data', 'anuncio_data', 'precio', 'cantidad', 'fechaInicio', 'fechaFin'
        ]

    def get_articulo(self, obj):
        if hasattr(obj, 'articulo'):
            return ArticuloSerializer(obj.articulo).data
        return None

    def get_anuncio(self, obj):
        if hasattr(obj, 'anuncio'):
            return AnuncioSerializer(obj.anuncio).data
        return None

    def create(self, validated_data):
        # Extraer datos anidados si vienen en modo JSON
        articulo_data = validated_data.pop('articulo_data', None)
        anuncio_data = validated_data.pop('anuncio_data', None)

        # Extraer datos planos si vienen en multipart
        precio = validated_data.pop('precio', None)
        cantidad = validated_data.pop('cantidad', None)
        fechaInicio = validated_data.pop('fechaInicio', None)
        fechaFin = validated_data.pop('fechaFin', None)

        publicacion = Publicacion.objects.create(**validated_data)

        # Prioridad: si vienen datos anidados se usan; si no, modo plano.
        if articulo_data:
            Articulo.objects.create(idPublicacion=publicacion, **articulo_data)
        elif anuncio_data:
            Anuncio.objects.create(idPublicacion=publicacion, **anuncio_data)
        else:
            # Modo plano
            if precio is not None and cantidad is not None:
                Articulo.objects.create(idPublicacion=publicacion, precio=precio, cantidad=cantidad)
            elif fechaInicio is not None and fechaFin is not None:
                Anuncio.objects.create(idPublicacion=publicacion, fechaInicio=fechaInicio, fechaFin=fechaFin)

        return publicacion

    def update(self, instance, validated_data):
        # Extraer datos anidados si vienen en modo JSON
        articulo_data = validated_data.pop('articulo_data', None)
        anuncio_data = validated_data.pop('anuncio_data', None)

        # Extraer datos planos si vienen en multipart
        precio = validated_data.pop('precio', None)
        cantidad = validated_data.pop('cantidad', None)
        fechaInicio = validated_data.pop('fechaInicio', None)
        fechaFin = validated_data.pop('fechaFin', None)

        # Actualizar campos de la publicación
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        if 'imagen' in validated_data:
            instance.imagen = validated_data['imagen']
        if 'subcategoria' in validated_data:
            instance.subcategoria = validated_data['subcategoria']
        instance.save()

        # Actualizar o crear artículo/anuncio si vienen datos
        if articulo_data:
            if hasattr(instance, 'articulo'):
                # Actualizar artículo existente
                articulo = instance.articulo
                articulo.precio = articulo_data.get('precio', articulo.precio)
                articulo.cantidad = articulo_data.get('cantidad', articulo.cantidad)
                articulo.save()
            else:
                # Crear nuevo artículo
                Articulo.objects.create(idPublicacion=instance, **articulo_data)
        elif precio is not None and cantidad is not None:
            if hasattr(instance, 'articulo'):
                # Actualizar artículo existente (modo plano)
                articulo = instance.articulo
                articulo.precio = precio
                articulo.cantidad = cantidad
                articulo.save()
            else:
                # Crear nuevo artículo (modo plano)
                Articulo.objects.create(idPublicacion=instance, precio=precio, cantidad=cantidad)

        if anuncio_data:
            if hasattr(instance, 'anuncio'):
                # Actualizar anuncio existente
                anuncio = instance.anuncio
                anuncio.fechaInicio = anuncio_data.get('fechaInicio', anuncio.fechaInicio)
                anuncio.fechaFin = anuncio_data.get('fechaFin', anuncio.fechaFin)
                anuncio.save()
            else:
                # Crear nuevo anuncio
                Anuncio.objects.create(idPublicacion=instance, **anuncio_data)
        elif fechaInicio is not None and fechaFin is not None:
            if hasattr(instance, 'anuncio'):
                # Actualizar anuncio existente (modo plano)
                anuncio = instance.anuncio
                anuncio.fechaInicio = fechaInicio
                anuncio.fechaFin = fechaFin
                anuncio.save()
            else:
                # Crear nuevo anuncio (modo plano)
                Anuncio.objects.create(idPublicacion=instance, fechaInicio=fechaInicio, fechaFin=fechaFin)

        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    publicaciones = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'publicaciones']
