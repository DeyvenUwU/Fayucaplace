from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import Profile
from posting.models import Publicacion, Categoria, SubCategoria, Anuncio, Articulo
from chat.models import Message


class Command(BaseCommand):
    help = 'Verifica el contenido de la base de datos'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("VERIFICACION DE BASE DE DATOS - FayucaPlace")
        self.stdout.write("=" * 60)
        
        # Usuarios
        users_count = User.objects.count()
        self.stdout.write(f"\n[USUARIOS]")
        self.stdout.write(f"   Total: {users_count}")
        if users_count > 0:
            self.stdout.write(f"   Usuarios:")
            for user in User.objects.all()[:10]:
                tipo = "Admin" if user.is_staff else "Usuario"
                self.stdout.write(f"      - {tipo}: {user.username} ({user.email})")
        
        # Perfiles
        profiles_count = Profile.objects.count()
        self.stdout.write(f"\n[PERFILES]")
        self.stdout.write(f"   Total: {profiles_count}")
        
        # Categorias
        categorias_count = Categoria.objects.count()
        self.stdout.write(f"\n[CATEGORIAS]")
        self.stdout.write(f"   Total: {categorias_count}")
        if categorias_count > 0:
            for cat in Categoria.objects.all():
                subcats = SubCategoria.objects.filter(categoria=cat).count()
                self.stdout.write(f"      - {cat.nombre} ({subcats} subcategorias)")
        
        # Subcategorias
        subcategorias_count = SubCategoria.objects.count()
        self.stdout.write(f"\n[SUBCATEGORIAS]")
        self.stdout.write(f"   Total: {subcategorias_count}")
        
        # Publicaciones
        publicaciones_count = Publicacion.objects.count()
        self.stdout.write(f"\n[PUBLICACIONES]")
        self.stdout.write(f"   Total: {publicaciones_count}")
        
        # Anuncios
        anuncios_count = Anuncio.objects.count()
        self.stdout.write(f"   Anuncios: {anuncios_count}")
        if anuncios_count > 0:
            self.stdout.write(f"   Ultimos anuncios:")
            for anuncio in Anuncio.objects.select_related('idPublicacion', 'idPublicacion__idUsuario')[:5]:
                self.stdout.write(f"      - {anuncio.idPublicacion.titulo} por {anuncio.idPublicacion.idUsuario.username}")
        
        # Articulos
        articulos_count = Articulo.objects.count()
        self.stdout.write(f"   Articulos: {articulos_count}")
        if articulos_count > 0:
            self.stdout.write(f"   Ultimos articulos:")
            for articulo in Articulo.objects.select_related('idPublicacion', 'idPublicacion__idUsuario')[:5]:
                precio = f"${articulo.precio}" if articulo.precio else "Sin precio"
                self.stdout.write(f"      - {articulo.idPublicacion.titulo} - {precio} por {articulo.idPublicacion.idUsuario.username}")
        
        # Mensajes
        mensajes_count = Message.objects.count()
        self.stdout.write(f"\n[MENSAJES]")
        self.stdout.write(f"   Total: {mensajes_count}")
        
        # Resumen
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("RESUMEN")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Usuarios: {users_count}")
        self.stdout.write(f"Perfiles: {profiles_count}")
        self.stdout.write(f"Categorias: {categorias_count}")
        self.stdout.write(f"Subcategorias: {subcategorias_count}")
        self.stdout.write(f"Publicaciones: {publicaciones_count}")
        self.stdout.write(f"   - Anuncios: {anuncios_count}")
        self.stdout.write(f"   - Articulos: {articulos_count}")
        self.stdout.write(f"Mensajes: {mensajes_count}")
        
        # Verificar datos necesarios
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("VERIFICACION DE DATOS NECESARIOS")
        self.stdout.write("=" * 60)
        
        issues = []
        
        if users_count == 0:
            issues.append("No hay usuarios. Crear superusuario: python manage.py createsuperuser")
        
        if categorias_count == 0:
            issues.append("No hay categorias. Ejecutar: python manage.py migrate")
        
        if not User.objects.filter(is_staff=True).exists():
            issues.append("No hay usuarios administradores. Crear uno con: python manage.py createsuperuser")
        
        if issues:
            self.stdout.write(self.style.WARNING("\nPROBLEMAS ENCONTRADOS:"))
            for issue in issues:
                self.stdout.write(self.style.WARNING(f"   - {issue}"))
        else:
            self.stdout.write(self.style.SUCCESS("\nTodo esta bien! La base de datos tiene los datos necesarios."))
        
        self.stdout.write("\n" + "=" * 60)
