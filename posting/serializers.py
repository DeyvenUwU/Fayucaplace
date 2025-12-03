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
