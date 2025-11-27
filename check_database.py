"""
Script para verificar el contenido de la base de datos de FayucaPlace
"""
from django.contrib.auth.models import User
from profiles.models import Profile
from posting.models import Publicacion, Categoria, SubCategoria, Anuncio, Articulo
from chat.models import Message

def check_database():
    print("=" * 60)
    print("VERIFICACIÓN DE BASE DE DATOS - FayucaPlace")
    print("=" * 60)
    
    # Usuarios
    users_count = User.objects.count()
    print(f"\n📊 USUARIOS")
    print(f"   Total: {users_count}")
    if users_count > 0:
        print(f"   Usuarios:")
        for user in User.objects.all()[:10]:
            tipo = "👑 Admin" if user.is_staff else "👤 Usuario"
            print(f"      - {tipo}: {user.username} ({user.email})")
    
    # Perfiles
    profiles_count = Profile.objects.count()
    print(f"\n👥 PERFILES")
    print(f"   Total: {profiles_count}")
    
    # Categorías
    categorias_count = Categoria.objects.count()
    print(f"\n📁 CATEGORÍAS")
    print(f"   Total: {categorias_count}")
    if categorias_count > 0:
        for cat in Categoria.objects.all():
            subcats = SubCategoria.objects.filter(categoria=cat).count()
            print(f"      - {cat.nombre} ({subcats} subcategorías)")
    
    # Subcategorías
    subcategorias_count = SubCategoria.objects.count()
    print(f"\n📂 SUBCATEGORÍAS")
    print(f"   Total: {subcategorias_count}")
    
    # Publicaciones
    publicaciones_count = Publicacion.objects.count()
    print(f"\n📝 PUBLICACIONES")
    print(f"   Total: {publicaciones_count}")
    
    # Anuncios
    anuncios_count = Anuncio.objects.count()
    print(f"   Anuncios: {anuncios_count}")
    if anuncios_count > 0:
        print(f"   Últimos anuncios:")
        for anuncio in Anuncio.objects.select_related('idPublicacion', 'idPublicacion__idUsuario')[:5]:
            print(f"      - {anuncio.idPublicacion.titulo} por {anuncio.idPublicacion.idUsuario.username}")
    
    # Artículos
    articulos_count = Articulo.objects.count()
    print(f"   Artículos: {articulos_count}")
    if articulos_count > 0:
        print(f"   Últimos artículos:")
        for articulo in Articulo.objects.select_related('idPublicacion', 'idPublicacion__idUsuario')[:5]:
            precio = f"${articulo.precio}" if articulo.precio else "Sin precio"
            print(f"      - {articulo.idPublicacion.titulo} - {precio} por {articulo.idPublicacion.idUsuario.username}")
    
    # Mensajes
    mensajes_count = Message.objects.count()
    print(f"\n💬 MENSAJES")
    print(f"   Total: {mensajes_count}")
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"✅ Usuarios: {users_count}")
    print(f"✅ Perfiles: {profiles_count}")
    print(f"✅ Categorías: {categorias_count}")
    print(f"✅ Subcategorías: {subcategorias_count}")
    print(f"✅ Publicaciones: {publicaciones_count}")
    print(f"   - Anuncios: {anuncios_count}")
    print(f"   - Artículos: {articulos_count}")
    print(f"✅ Mensajes: {mensajes_count}")
    
    # Verificar datos necesarios
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE DATOS NECESARIOS")
    print("=" * 60)
    
    issues = []
    
    if users_count == 0:
        issues.append("⚠️  No hay usuarios. Crear superusuario: python manage.py createsuperuser")
    
    if categorias_count == 0:
        issues.append("⚠️  No hay categorías. Ejecutar: python manage.py migrate")
    
    if not User.objects.filter(is_staff=True).exists():
        issues.append("⚠️  No hay usuarios administradores. Crear uno con: python manage.py createsuperuser")
    
    if issues:
        print("\n❌ PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ ¡Todo está bien! La base de datos tiene los datos necesarios.")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_database()
