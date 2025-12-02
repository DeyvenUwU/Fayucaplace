from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'publicaciones', api_views.PublicacionViewSet, basename='publicacion')
router.register(r'profiles', api_views.ProfileViewSet, basename='profile')
router.register(r'users', api_views.UserViewSet, basename='user')
router.register(r'categorias', api_views.CategoriaViewSet, basename='categoria')
router.register(r'subcategorias', api_views.SubCategoriaViewSet, basename='subcategoria')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
