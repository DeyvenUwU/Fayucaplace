from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Categoria = apps.get_model('posting', 'Categoria')
    SubCategoria = apps.get_model('posting', 'SubCategoria')

    # Categoría 1: Electrónica
    electronica = Categoria.objects.create(nombre='Electrónica')
    SubCategoria.objects.create(categoria=electronica, nombre='Smartphones')
    SubCategoria.objects.create(categoria=electronica, nombre='Laptops')
    SubCategoria.objects.create(categoria=electronica, nombre='Televisores')

    # Categoría 2: Ropa y Accesorios
    ropa = Categoria.objects.create(nombre='Ropa y Accesorios')
    SubCategoria.objects.create(categoria=ropa, nombre='Camisetas')
    SubCategoria.objects.create(categoria=ropa, nombre='Pantalones')
    SubCategoria.objects.create(categoria=ropa, nombre='Zapatos')

    # Categoría 3: Hogar y Jardín
    hogar = Categoria.objects.create(nombre='Hogar y Jardín')
    SubCategoria.objects.create(categoria=hogar, nombre='Muebles')
    SubCategoria.objects.create(categoria=hogar, nombre='Decoración')
    SubCategoria.objects.create(categoria=hogar, nombre='Herramientas')


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_categoria_subcategoria_publicacion_subcategoria'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]
