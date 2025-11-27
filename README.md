# FayucaPlace

Marketplace y tablero de anuncios construido con Django + Django REST Framework.

## Características principales
- Modelos relacionados: usuarios, perfiles, publicaciones, artículos, anuncios, categorías, subcategorías, chats y mensajes.
- **Autenticación**: sesiones Django + Token Auth (DRF) + grupos/permisos
- **Autorización**: roles (Admin, Vendedor, Comprador) con permisos granulares
- **Seguridad**: CSRF, XSS, SQL Injection protection, HTTPS/HSTS, secure cookies
- CRUD API REST para publicaciones, categorías y subcategorías
- Búsqueda y filtrado: parámetros `search`, `subcategoria`, `anuncio__isnull`, `articulo__isnull`
- Subida de imágenes para publicaciones (multipart/form-data)
- AJAX (fetch) para crear, editar y eliminar publicaciones
- Dashboard con gráficas (Chart.js) para métricas básicas
- Exportación a PDF (WeasyPrint) y Excel (openpyxl)
- CI/CD con GitHub Actions

## Requisitos
Python 3.11+, Django 5.x, Django REST Framework, Pillow, WeasyPrint, openpyxl, Gunicorn, PostgreSQL (producción).

## Instalación (desarrollo)
```powershell
# Windows PowerShell
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < setup_permissions.py  # Configurar grupos y permisos
python manage.py createsuperuser
python manage.py runserver
```

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < setup_permissions.py
python manage.py createsuperuser
python manage.py runserver
```

## Seguridad implementada
Ver [SECURITY.md](SECURITY.md) para detalles completos.

**5 aspectos clave:**
1. **CSRF**: Tokens en formularios, CSRF_COOKIE_HTTPONLY
2. **XSS**: Auto-escape templates, security headers
3. **CORS**: Same-origin por defecto
4. **SQL Injection**: ORM con queries parametrizadas
5. **Host/Referrer**: ALLOWED_HOSTS validation, CSRF_TRUSTED_ORIGINS

**Autenticación/Autorización:**
- Login requerido en vistas sensibles (`@login_required`)
- Grupos: Admin (todos los permisos), Vendedor (CRUD publicaciones), Comprador (solo lectura)
- Permisos por objeto: usuarios solo editan sus propias publicaciones
- Decoradores personalizados: `@admin_required`, mixins `AdminRequiredMixin`
- API: `IsOwnerOrReadOnly`, TokenAuthentication, throttling

## Variables de entorno (producción)
```bash
export DJANGO_SECRET_KEY="tu_clave_muy_segura_aqui"
export DEBUG="False"
export ALLOWED_HOSTS="tu-dominio.com,www.tu-dominio.com"
export CSRF_TRUSTED_ORIGINS="https://tu-dominio.com,https://www.tu-dominio.com"
export DATABASE_URL="postgres://user:pass@host:5432/fayuca"
```

## Deployment (producción)
Ver [DEPLOYMENT.md](DEPLOYMENT.md) para checklist completo y comandos.

### Quick start con Gunicorn + Nginx (Linux)
```bash
# 1. Instalar dependencias sistema
sudo apt update && sudo apt install python3-pip python3-venv nginx postgresql

# 2. Configurar PostgreSQL
sudo -u postgres createdb fayucaplace
sudo -u postgres createuser fayuca_user
sudo -u postgres psql -c "ALTER USER fayuca_user WITH PASSWORD 'secure_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fayucaplace TO fayuca_user;"

# 3. Clonar y setup
git clone https://github.com/DeyvenUwU/Fayucaplace.git
cd Fayucaplace
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Variables de entorno y migraciones
export DJANGO_SECRET_KEY="..."
export DEBUG="False"
export ALLOWED_HOSTS="tu-dominio.com"
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell < setup_permissions.py

# 5. Configurar servicios
sudo cp fayucaplace.service /etc/systemd/system/
sudo cp nginx_fayuca.conf /etc/nginx/sites-available/fayucaplace
sudo ln -s /etc/nginx/sites-available/fayucaplace /etc/nginx/sites-enabled/
sudo systemctl daemon-reload
sudo systemctl start fayucaplace
sudo systemctl enable fayucaplace
sudo systemctl restart nginx
```

### Deployment con ngrok (testing/demo)
```bash
# Instalar ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Autenticar
ngrok config add-authtoken <tu-token>

# Ejecutar app
python manage.py runserver 0.0.0.0:8000

# En otra terminal, exponer con ngrok
ngrok http 8000

# Actualizar ALLOWED_HOSTS con URL de ngrok (ej: abc123.ngrok.io)
export ALLOWED_HOSTS="abc123.ngrok.io,localhost"
export CSRF_TRUSTED_ORIGINS="https://abc123.ngrok.io"
```

### Plataformas cloud
- **Railway**: Auto-deploy desde GitHub, PostgreSQL incluido
- **Render**: Free tier, auto-deploy
- **Heroku**: Requiere Procfile
- **DigitalOcean/AWS/GCP**: VPS con control completo

## Endpoints API principales
Base: `/api/`
- `publicaciones/` (GET, POST) ; `publicaciones/<id>/` (GET, PUT, DELETE)
- `categorias/` (CRUD completo)
- `subcategorias/` (CRUD completo, filtro `?categoria=<id>`)
- `profiles/` (GET, POST, PUT)
- `users/` (GET, solo lectura)

**Autenticación API:**
```bash
# Obtener token
curl -X POST http://localhost:8000/api-token-auth/ -d "username=user&password=pass"

# Usar token
curl -H "Authorization: Token abc123..." http://localhost:8000/api/publicaciones/
```

## Dashboard y reportes
- Dashboard: `/dashboard/` (gráficas con Chart.js)
- Export PDF: `/export/pdf/` (requiere rol Admin)
- Export Excel: `/export/excel/` (requiere rol Admin)

## Tests
```bash
python manage.py test posting
python manage.py check --deploy  # Verificar configuración producción
```

## CI/CD
GitHub Actions configurado en `.github/workflows/deploy.yml`:
- Tests automáticos en push/PR
- Deploy automático a producción en merge a master
- Verificación de deployment readiness

## Estructura del proyecto
```
Fayucaplace/
├── mysite/               # Configuración principal
│   ├── settings.py       # Settings desarrollo
│   ├── settings_prod.py  # Settings producción
│   ├── permissions.py    # Mixins y decoradores
│   └── urls.py
├── posting/              # App publicaciones
│   ├── models.py
│   ├── views.py
│   ├── api_views.py      # ViewSets DRF
│   ├── serializers.py
│   ├── permissions.py    # IsOwnerOrReadOnly
│   └── tests.py
├── profiles/             # App perfiles
├── chat/                 # App mensajería
├── static/               # Assets estáticos
├── media/                # Archivos subidos
├── templates/            # Plantillas HTML
├── gunicorn_config.py    # Config Gunicorn
├── nginx_fayuca.conf     # Config Nginx
├── fayucaplace.service   # Systemd service
├── setup_permissions.py  # Script grupos/permisos
├── SECURITY.md           # Documentación seguridad
├── DEPLOYMENT.md         # Checklist deployment
└── requirements.txt
```

## Grupos y permisos
Ejecutar `python manage.py shell < setup_permissions.py` para crear:

**Admin**: Todos los permisos (crear/editar/borrar publicaciones y categorías)
**Vendedor**: Crear y editar publicaciones propias
**Comprador**: Solo lectura de publicaciones

Asignar grupo a usuario en admin Django o:
```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='username')
group = Group.objects.get(name='Vendedor')
user.groups.add(group)
```

## Troubleshooting

**502 Bad Gateway**: Verificar Gunicorn está ejecutándose
```bash
sudo systemctl status fayucaplace
sudo journalctl -u fayucaplace -n 50
```

**CSRF Failed**: Agregar dominio a CSRF_TRUSTED_ORIGINS

**Static files 404**: Ejecutar `collectstatic`
```bash
python manage.py collectstatic --noinput
```

**Permission denied**: Verificar permisos de archivos
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/Fayucaplace
chmod -R 755 /home/ubuntu/Fayucaplace
```

## Contribuir
1. Fork del repositorio
2. Crear branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar funcionalidad'`)
4. Push a branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia
Proyecto educativo / interno. Ajustar antes de hacer público.
