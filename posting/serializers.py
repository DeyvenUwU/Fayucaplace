<<<<<<< HEAD
<<<<<<< HEAD
from rest_framework import serializers
from django.contrib.auth.models import User
from django.urls import reverse
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
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    subcategoria_nombre = serializers.CharField(source='subCategoria.nombre', read_only=True)
    
    class Meta:
        model = Articulo
        fields = ['precio', 'cantidad', 'categoria', 'subCategoria', 'condicion', 'categoria_nombre', 'subcategoria_nombre']

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = ['fechaInicio', 'fechaFin']

class PublicacionSerializer(serializers.ModelSerializer):
    articulo = ArticuloSerializer(required=False)
    anuncio = AnuncioSerializer(required=False)
    idUsuario = serializers.ReadOnlyField(source='idUsuario.username')
    imagen_url = serializers.SerializerMethodField(read_only=True)
    imagen = serializers.ImageField(required=False, allow_null=True)
    
    # Para manejar FormData plano
    precio = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, write_only=True)
    cantidad = serializers.IntegerField(required=False, write_only=True)
    categoria = serializers.IntegerField(required=False, write_only=True)
    subCategoria = serializers.IntegerField(required=False, write_only=True)
    condicion = serializers.CharField(required=False, write_only=True)
    fechaInicio = serializers.DateField(required=False, write_only=True)
    fechaFin = serializers.DateField(required=False, write_only=True)
    
    def get_imagen_url(self, obj):
        """Devuelve la URL relativa de la imagen si existe"""
        if obj.imagen:
            return obj.imagen.url
        return None

    class Meta:
        model = Publicacion
        fields = ['id', 'titulo', 'imagen', 'imagen_url', 'descripcion', 'idUsuario', 'fechaPublicacion', 'estado', 'articulo', 'anuncio', 'precio', 'cantidad', 'categoria', 'subCategoria', 'condicion', 'fechaInicio', 'fechaFin']

    def create(self, validated_data):
        # Extraer datos de FormData plano si existen
        precio = validated_data.pop('precio', None)
        cantidad = validated_data.pop('cantidad', None)
        categoria_id = validated_data.pop('categoria', None)
        subCategoria_id = validated_data.pop('subCategoria', None)
        condicion = validated_data.pop('condicion', None)
        fechaInicio = validated_data.pop('fechaInicio', None)
        fechaFin = validated_data.pop('fechaFin', None)
        
        # Extraer datos de JSON anidado si existen
        articulo_data = validated_data.pop('articulo', None)
        anuncio_data = validated_data.pop('anuncio', None)
        
        publicacion = Publicacion.objects.create(**validated_data)
        
        # Si vienen datos de FormData plano, crear los modelos relacionados
        if precio is not None and cantidad is not None:
            Articulo.objects.create(
                idPublicacion=publicacion, 
                precio=precio, 
                cantidad=cantidad,
                categoria_id=categoria_id,
                subCategoria_id=subCategoria_id,
                condicion=condicion or 'USADO'
            )
        elif articulo_data:
            Articulo.objects.create(idPublicacion=publicacion, **articulo_data)
        elif fechaInicio is not None and fechaFin is not None:
            Anuncio.objects.create(idPublicacion=publicacion, fechaInicio=fechaInicio, fechaFin=fechaFin)
        elif anuncio_data:
            Anuncio.objects.create(idPublicacion=publicacion, **anuncio_data)
            
        return publicacion

    def update(self, instance, validated_data):
        # Extraer datos de FormData plano si existen
        precio = validated_data.pop('precio', None)
        cantidad = validated_data.pop('cantidad', None)
        categoria_id = validated_data.pop('categoria', None)
        subCategoria_id = validated_data.pop('subCategoria', None)
        condicion = validated_data.pop('condicion', None)
        fechaInicio = validated_data.pop('fechaInicio', None)
        fechaFin = validated_data.pop('fechaFin', None)
        
        # Si no hay imagen nueva, mantener la existente
        if 'imagen' in validated_data and validated_data['imagen'] is None:
            validated_data.pop('imagen')
        
        # Actualizar campos de Publicacion
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar Articulo si existen datos
        if precio is not None or cantidad is not None or categoria_id is not None or subCategoria_id is not None or condicion is not None:
            try:
                articulo = instance.articulo
                if precio is not None:
                    articulo.precio = precio
                if cantidad is not None:
                    articulo.cantidad = cantidad
                if categoria_id is not None:
                    articulo.categoria_id = categoria_id
                if subCategoria_id is not None:
                    articulo.subCategoria_id = subCategoria_id
                if condicion is not None:
                    articulo.condicion = condicion
                articulo.save()
            except Articulo.DoesNotExist:
                pass
        
        # Actualizar Anuncio si existen datos
        if fechaInicio is not None or fechaFin is not None:
            try:
                anuncio = instance.anuncio
                if fechaInicio is not None:
                    anuncio.fechaInicio = fechaInicio
                if fechaFin is not None:
                    anuncio.fechaFin = fechaFin
                anuncio.save()
            except Anuncio.DoesNotExist:
                pass
        
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
=======
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
    articulo = ArticuloSerializer(required=False)
    anuncio = AnuncioSerializer(required=False)
    idUsuario = serializers.ReadOnlyField(source='idUsuario.username')
    subcategoria = serializers.StringRelatedField()

    class Meta:
        model = Publicacion
        fields = ['id', 'titulo', 'imagen', 'descripcion', 'idUsuario', 'fechaPublicacion', 'estado', 'subcategoria', 'articulo', 'anuncio']

    def create(self, validated_data):
        articulo_data = validated_data.pop('articulo', None)
        anuncio_data = validated_data.pop('anuncio', None)
        
        publicacion = Publicacion.objects.create(**validated_data)
        
        if articulo_data:
            Articulo.objects.create(idPublicacion=publicacion, **articulo_data)
        elif anuncio_data:
            Anuncio.objects.create(idPublicacion=publicacion, **anuncio_data)
            
        return publicacion

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    publicaciones = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'publicaciones']
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
=======
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
    articulo = ArticuloSerializer(required=False)
    anuncio = AnuncioSerializer(required=False)
    idUsuario = serializers.ReadOnlyField(source='idUsuario.username')
    subcategoria = serializers.StringRelatedField()

    class Meta:
        model = Publicacion
        fields = ['id', 'titulo', 'imagen', 'descripcion', 'idUsuario', 'fechaPublicacion', 'estado', 'subcategoria', 'articulo', 'anuncio']

    def create(self, validated_data):
        articulo_data = validated_data.pop('articulo', None)
        anuncio_data = validated_data.pop('anuncio', None)
        
        publicacion = Publicacion.objects.create(**validated_data)
        
        if articulo_data:
            Articulo.objects.create(idPublicacion=publicacion, **articulo_data)
        elif anuncio_data:
            Anuncio.objects.create(idPublicacion=publicacion, **anuncio_data)
            
        return publicacion

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    publicaciones = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'publicaciones']
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
