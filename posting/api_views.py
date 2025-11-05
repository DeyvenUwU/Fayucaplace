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
