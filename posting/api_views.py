<<<<<<< HEAD
<<<<<<< HEAD
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import Publicacion, Categoria, SubCategoria
from .serializers import PublicacionSerializer, ProfileSerializer, UserSerializer, CategoriaSerializer, SubCategoriaSerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from django.utils import timezone
from datetime import date

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SubCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subcategories to be viewed.
    Accepts a 'categoria' query parameter to filter by category id.
    """
    serializer_class = SubCategoriaSerializer

    def get_queryset(self):
        queryset = SubCategoria.objects.all()
        category_id = self.request.query_params.get('categoria', None)
        if category_id is not None:
            queryset = queryset.filter(categoria__id=category_id)
        return queryset

class PublicacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Publicacion.objects.all()
        search = self.request.query_params.get('search', None)
        subcategoria = self.request.query_params.get('subcategoria', None)
        anuncio_isnull = self.request.query_params.get('anuncio__isnull', None)
        articulo_isnull = self.request.query_params.get('articulo__isnull', None)
        include_paused = self.request.query_params.get('include_paused', 'false').lower() == 'true'
        
        # Filtros adicionales para artículos
        condicion = self.request.query_params.get('condicion', None)
        precio_min = self.request.query_params.get('precio_min', None)
        precio_max = self.request.query_params.get('precio_max', None)
        ordenar = self.request.query_params.get('ordenar', None)

        # Solo mostrar publicaciones activas a menos que se pida explícitamente incluir pausadas
        if not include_paused:
            queryset = queryset.filter(estado='ACTIVA')

        if search is not None:
            queryset = queryset.filter(titulo__icontains=search)
        
        if subcategoria is not None:
            # Filtrar por subcategoría del artículo
            queryset = queryset.filter(articulo__subCategoria__id=subcategoria)

        if anuncio_isnull is not None:
            if anuncio_isnull == 'false':
                # Solo mostrar anuncios vigentes (fecha actual dentro del rango)
                hoy = date.today()
                queryset = queryset.filter(
                    anuncio__isnull=False,
                    anuncio__fechaInicio__lte=hoy,
                    anuncio__fechaFin__gte=hoy
                )
            else:
                queryset = queryset.filter(anuncio__isnull=True)

        if articulo_isnull is not None:
            queryset = queryset.filter(articulo__isnull=articulo_isnull == 'true')
        
        # Filtrar por condición del artículo
        if condicion is not None:
            queryset = queryset.filter(articulo__condicion=condicion)
        
        # Filtrar por rango de precios
        if precio_min is not None:
            queryset = queryset.filter(articulo__precio__gte=precio_min)
        if precio_max is not None:
            queryset = queryset.filter(articulo__precio__lte=precio_max)
        
        # Ordenar por precio
        if ordenar == 'precio_asc':
            queryset = queryset.order_by('articulo__precio')
        elif ordenar == 'precio_desc':
            queryset = queryset.order_by('-articulo__precio')
        else:
            queryset = queryset.order_by('-fechaPublicacion')

        return queryset

    def get_object(self):
        """
        Retrieve an object instance. Allow owners to retrieve paused publications
        so they can update/reactivate them. For non-owners, enforce the
        "only active unless include_paused=true" rule.
        """
        pk = self.kwargs.get(self.lookup_field or 'pk')
        obj = get_object_or_404(Publicacion.objects.all(), pk=pk)

        include_paused = self.request.query_params.get('include_paused', 'false').lower() == 'true'

        # If the publication is paused and the requester is NOT the owner and
        # hasn't explicitly asked to include paused posts, hide it.
        if obj.estado == 'PAUSADA' and not include_paused:
            # Allow owner to access paused object for update/retrieve
            if not self.request.user.is_authenticated or obj.idUsuario != self.request.user:
                raise NotFound()

        # Run permission checks
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(idUsuario=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
=======
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import Publicacion, Categoria, SubCategoria
from .serializers import PublicacionSerializer, ProfileSerializer, UserSerializer, CategoriaSerializer, SubCategoriaSerializer
from .permissions import IsOwnerOrReadOnly

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SubCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subcategories to be viewed.
    Accepts a 'categoria' query parameter to filter by category id.
    """
    serializer_class = SubCategoriaSerializer

    def get_queryset(self):
        queryset = SubCategoria.objects.all()
        category_id = self.request.query_params.get('categoria', None)
        if category_id is not None:
            queryset = queryset.filter(categoria__id=category_id)
        return queryset

class PublicacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Publicacion.objects.all().order_by('-fechaPublicacion')
        search = self.request.query_params.get('search', None)
        subcategoria = self.request.query_params.get('subcategoria', None)
        anuncio_isnull = self.request.query_params.get('anuncio__isnull', None)
        articulo_isnull = self.request.query_params.get('articulo__isnull', None)

        if search is not None:
            queryset = queryset.filter(titulo__icontains=search)
        
        if subcategoria is not None:
            queryset = queryset.filter(subcategoria__id=subcategoria)

        if anuncio_isnull is not None:
            queryset = queryset.filter(anuncio__isnull=anuncio_isnull == 'true')

        if articulo_isnull is not None:
            queryset = queryset.filter(articulo__isnull=articulo_isnull == 'true')

        return queryset

    def perform_create(self, serializer):
        serializer.save(idUsuario=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
=======
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import Publicacion, Categoria, SubCategoria
from .serializers import PublicacionSerializer, ProfileSerializer, UserSerializer, CategoriaSerializer, SubCategoriaSerializer
from .permissions import IsOwnerOrReadOnly

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SubCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subcategories to be viewed.
    Accepts a 'categoria' query parameter to filter by category id.
    """
    serializer_class = SubCategoriaSerializer

    def get_queryset(self):
        queryset = SubCategoria.objects.all()
        category_id = self.request.query_params.get('categoria', None)
        if category_id is not None:
            queryset = queryset.filter(categoria__id=category_id)
        return queryset

class PublicacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    serializer_class = PublicacionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Publicacion.objects.all().order_by('-fechaPublicacion')
        search = self.request.query_params.get('search', None)
        subcategoria = self.request.query_params.get('subcategoria', None)
        anuncio_isnull = self.request.query_params.get('anuncio__isnull', None)
        articulo_isnull = self.request.query_params.get('articulo__isnull', None)

        if search is not None:
            queryset = queryset.filter(titulo__icontains=search)
        
        if subcategoria is not None:
            queryset = queryset.filter(subcategoria__id=subcategoria)

        if anuncio_isnull is not None:
            queryset = queryset.filter(anuncio__isnull=anuncio_isnull == 'true')

        if articulo_isnull is not None:
            queryset = queryset.filter(articulo__isnull=articulo_isnull == 'true')

        return queryset

    def perform_create(self, serializer):
        serializer.save(idUsuario=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
>>>>>>> f271bf24dfb35a8596c07af58ada957384fefd36
