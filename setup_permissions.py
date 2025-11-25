"""
Script de inicialización de grupos y permisos.
Ejecutar: python manage.py shell < setup_permissions.py
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from posting.models import Publicacion, Categoria, SubCategoria

# Crear grupos
admin_group, _ = Group.objects.get_or_create(name='Admin')
vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
comprador_group, _ = Group.objects.get_or_create(name='Comprador')

# Permisos para Publicacion
publicacion_ct = ContentType.objects.get_for_model(Publicacion)
add_pub = Permission.objects.get(codename='add_publicacion', content_type=publicacion_ct)
change_pub = Permission.objects.get(codename='change_publicacion', content_type=publicacion_ct)
delete_pub = Permission.objects.get(codename='delete_publicacion', content_type=publicacion_ct)
view_pub = Permission.objects.get(codename='view_publicacion', content_type=publicacion_ct)

# Permisos para Categoria/SubCategoria
categoria_ct = ContentType.objects.get_for_model(Categoria)
add_cat = Permission.objects.get(codename='add_categoria', content_type=categoria_ct)
change_cat = Permission.objects.get(codename='change_categoria', content_type=categoria_ct)
delete_cat = Permission.objects.get(codename='delete_categoria', content_type=categoria_ct)

# Admin: todos los permisos
admin_group.permissions.set([add_pub, change_pub, delete_pub, view_pub, add_cat, change_cat, delete_cat])

# Vendedor: puede crear y editar sus propias publicaciones
vendedor_group.permissions.set([add_pub, change_pub, view_pub])

# Comprador: solo visualizar
comprador_group.permissions.set([view_pub])

print("Grupos y permisos configurados correctamente.")
print("Admin: todos los permisos")
print("Vendedor: crear/editar publicaciones")
print("Comprador: solo ver publicaciones")
