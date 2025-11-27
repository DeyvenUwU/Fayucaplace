# Guía de acceso rápido - FayucaPlace

## URLs principales (desarrollo)

### Sitio público
- **Home**: http://127.0.0.1:8000/
- **Registro**: http://127.0.0.1:8000/signup/
- **Login**: http://127.0.0.1:8000/login/
- **Panel principal (anuncios)**: http://127.0.0.1:8000/mainpanel/
- **Comprar (artículos)**: http://127.0.0.1:8000/buy/
- **Nueva publicación artículo**: http://127.0.0.1:8000/newarticle/
- **Nuevo anuncio**: http://127.0.0.1:8000/newad/
- **Chat**: http://127.0.0.1:8000/chat/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Editar perfil**: http://127.0.0.1:8000/editprofile/

### Administración
- **Admin Django**: http://127.0.0.1:8000/admin/

### API REST
- **Base API**: http://127.0.0.1:8000/api/
- **Publicaciones**: http://127.0.0.1:8000/api/publicaciones/
- **Categorías**: http://127.0.0.1:8000/api/categorias/
- **Subcategorías**: http://127.0.0.1:8000/api/subcategorias/
- **Perfiles**: http://127.0.0.1:8000/api/profiles/
- **Usuarios**: http://127.0.0.1:8000/api/users/
- **Auth Token**: http://127.0.0.1:8000/api-token-auth/

### Exportaciones (requiere admin)
- **Export PDF**: http://127.0.0.1:8000/export/pdf/
- **Export Excel**: http://127.0.0.1:8000/export/excel/

## Usuarios de prueba

### Crear superusuario
```powershell
python manage.py createsuperuser
```
Ingresar:
- Username: admin
- Email: admin@fayuca.com
- Password: (mínimo 8 caracteres)

### Crear usuario regular
1. Ir a http://127.0.0.1:8000/signup/
2. Llenar formulario
3. Se crea automáticamente perfil asociado

### Asignar grupos
```python
# En manage.py shell
from django.contrib.auth.models import User, Group

# Crear usuario vendedor
user = User.objects.get(username='usuario')
vendedor = Group.objects.get(name='Vendedor')
user.groups.add(vendedor)

# Crear usuario comprador
user2 = User.objects.get(username='usuario2')
comprador = Group.objects.get(name='Comprador')
user2.groups.add(comprador)
```

## Flujos de prueba

### Flujo 1: Usuario comprador
1. Registrarse en /signup/
2. Login en /login/
3. Ver anuncios en /mainpanel/
4. Ver artículos en /buy/
5. Buscar publicaciones (barra de búsqueda)
6. Ver detalles de publicación
7. Enviar mensaje al vendedor
8. Ver chat en /chat/

### Flujo 2: Usuario vendedor
1. Login
2. Crear artículo en /newarticle/
   - Seleccionar categoría → se cargan subcategorías (AJAX)
   - Subir imagen
   - Ingresar precio y cantidad
3. Ver artículo publicado en /buy/
4. Editar publicación en /publication/<id>/edit/ (PUT AJAX)
5. Ver métricas en /dashboard/

### Flujo 3: Administrador
1. Login en /admin/
2. Gestionar usuarios, grupos, permisos
3. Gestionar categorías y subcategorías
4. Ver dashboard en /dashboard/
5. Exportar reportes:
   - PDF: /export/pdf/
   - Excel: /export/excel/
6. Usar API con privilegios completos

### Flujo 4: API externa
1. Obtener token:
   ```bash
   curl -X POST http://localhost:8000/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username":"user","password":"pass"}'
   ```

2. Listar publicaciones:
   ```bash
   curl -H "Authorization: Token abc123..." \
     http://localhost:8000/api/publicaciones/
   ```

3. Crear publicación (multipart):
   ```bash
   curl -X POST http://localhost:8000/api/publicaciones/ \
     -H "Authorization: Token abc123..." \
     -F "titulo=Test" \
     -F "descripcion=Desc" \
     -F "subcategoria=1" \
     -F "precio=100" \
     -F "cantidad=5" \
     -F "imagen=@foto.jpg"
   ```

4. Actualizar publicación:
   ```bash
   curl -X PUT http://localhost:8000/api/publicaciones/1/ \
     -H "Authorization: Token abc123..." \
     -F "titulo=Nuevo titulo"
   ```

5. Eliminar publicación:
   ```bash
   curl -X DELETE http://localhost:8000/api/publicaciones/1/ \
     -H "Authorization: Token abc123..."
   ```

## Aspectos de seguridad a probar

### CSRF
1. Intentar POST sin token → debe rechazar
2. Ver token en formularios con inspector de navegador

### XSS
1. Intentar insertar `<script>alert('XSS')</script>` en título
2. Verificar que se escapa automáticamente en HTML

### SQL Injection
1. Intentar búsqueda con: `' OR '1'='1`
2. Verificar que no afecta la consulta (ORM protege)

### Host Header
1. Configurar ALLOWED_HOSTS con dominio específico
2. Intentar acceder con Host header diferente → debe rechazar

### Permisos
1. Usuario comprador intenta acceder a /export/pdf/ → 403 Forbidden
2. Usuario no dueño intenta editar publicación ajena → 403 Forbidden
3. Usuario no autenticado intenta API → solo lectura

### Rate Limiting (producción)
1. Hacer más de 100 requests anónimas en un día
2. Verificar throttle 429 Too Many Requests

## Variables de entorno para testing local

```powershell
# PowerShell
$env:DEBUG = "True"
$env:ALLOWED_HOSTS = "localhost,127.0.0.1"

# Generar nueva SECRET_KEY
python generate_secret_key.py
$env:DJANGO_SECRET_KEY = "la-clave-generada"
```

## Troubleshooting común

### Error: CSRF verification failed
- Verificar que formulario tiene `{% csrf_token %}`
- Verificar CSRF_TRUSTED_ORIGINS incluye el dominio
- Limpiar cookies del navegador

### Error: 403 Forbidden en API
- Verificar token de autenticación
- Verificar permisos del usuario
- Verificar que usuario es dueño del objeto

### Error: Static files 404
- Ejecutar `collectstatic` si DEBUG=False
- Verificar STATIC_URL y STATICFILES_DIRS

### Error: Template not found
- Verificar que APP_DIRS = True en TEMPLATES
- Verificar que app está en INSTALLED_APPS

## Comandos útiles de debugging

```powershell
# Ver configuración actual
python manage.py diffsettings

# Shell interactivo
python manage.py shell

# Crear datos de prueba
python manage.py loaddata fixture.json

# Ver rutas disponibles
python manage.py show_urls  # Requiere django-extensions

# Ejecutar servidor con logs verbosos
python manage.py runserver --verbosity 3
```

## Métricas de verificación

- [ ] Usuario puede registrarse y hacer login
- [ ] Usuario puede crear publicación con imagen
- [ ] Dropdown categoría→subcategoría funciona (AJAX)
- [ ] Búsqueda dinámica funciona
- [ ] Usuario puede editar su publicación
- [ ] Usuario NO puede editar publicación ajena
- [ ] Admin puede exportar PDF y Excel
- [ ] Usuario regular NO puede exportar
- [ ] Dashboard muestra gráficas correctamente
- [ ] Chat funciona entre usuarios
- [ ] API responde correctamente con token
- [ ] Tests pasan: `python manage.py test`
- [ ] Check deployment no muestra errores críticos

## Acceso remoto (ngrok)

```bash
# Terminal 1: Iniciar servidor
python manage.py runserver 0.0.0.0:8000

# Terminal 2: Exponer con ngrok
ngrok http 8000

# Copiar URL (ej: https://abc123.ngrok.io)
# Actualizar variables:
export ALLOWED_HOSTS="abc123.ngrok.io,localhost"
export CSRF_TRUSTED_ORIGINS="https://abc123.ngrok.io"

# Compartir URL con evaluadores/clientes
```

## Contacto y soporte
- Repositorio: https://github.com/DeyvenUwU/Fayucaplace
- Documentación: README.md, SECURITY.md, DEPLOYMENT.md
- Issues: GitHub Issues
