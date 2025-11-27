from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views, views

# Router de la API. Antes se montaba bajo 'api/' aquí y luego nuevamente en `mysite/urls.py`,
# provocando que la ruta real fuera /api/api/publicaciones/ y las peticiones a /api/publicaciones/ dieran 404.
# Eliminamos el prefijo redundante para que `mysite/urls.py` maneje el prefijo único `/api/`.
router = DefaultRouter()
router.register(r'publicaciones', api_views.PublicacionViewSet, basename='publicacion')
router.register(r'profiles', api_views.ProfileViewSet, basename='profile')
router.register(r'users', api_views.UserViewSet, basename='user')
router.register(r'categorias', api_views.CategoriaViewSet, basename='categoria')
router.register(r'subcategorias', api_views.SubCategoriaViewSet, basename='subcategoria')

urlpatterns = [
    # Exponemos directamente las rutas del router; el prefijo /api/ lo añade `mysite/urls.py`.
    path('', include(router.urls)),
    path('export/excel/', views.export_articles_to_excel, name='export_excel'),
    # path('export/pdf/', views.export_articles_to_pdf, name='export_pdf'),  # Comentado temporalmente
]
