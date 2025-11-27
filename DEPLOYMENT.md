# Deployment Checklist para FayucaPlace

## Seguridad

### Configuración básica
- [x] SECRET_KEY movida a variable de entorno
- [x] DEBUG = False en producción
- [x] ALLOWED_HOSTS configurado
- [x] CSRF_COOKIE_SECURE = True
- [x] SESSION_COOKIE_SECURE = True
- [x] SECURE_SSL_REDIRECT = True
- [x] SECURE_HSTS_SECONDS configurado
- [x] X_FRAME_OPTIONS = 'DENY'
- [x] SECURE_CONTENT_TYPE_NOSNIFF = True

### Protecciones implementadas
- [x] **CSRF**: Middleware activo, tokens en formularios, CSRF_COOKIE_HTTPONLY
- [x] **XSS**: Escape automático templates, SECURE_BROWSER_XSS_FILTER
- [x] **SQL Injection**: ORM Django (prevención automática)
- [x] **Host Header**: ALLOWED_HOSTS validado, USE_X_FORWARDED_HOST controlado
- [x] **CORS**: Sin configuración por defecto (agregar django-cors-headers si se necesita API pública)

### Autenticación y autorización
- [x] Login requerido en vistas sensibles (@login_required)
- [x] Grupos y permisos: Admin, Vendedor, Comprador
- [x] Permisos por objeto (IsOwnerOrReadOnly en API)
- [x] Decorador @admin_required para exportaciones
- [x] Mixins para vistas basadas en clases

## Base de datos
- [ ] Migrar de SQLite a PostgreSQL/MySQL
- [x] Migraciones aplicadas
- [ ] Backup automático configurado

## Archivos estáticos y media
- [x] STATIC_ROOT configurado
- [ ] collectstatic ejecutado
- [x] MEDIA_ROOT configurado
- [ ] Permisos de escritura verificados

## Servidor web
- [x] Gunicorn config creado
- [x] Nginx config creado
- [x] Systemd service creado
- [ ] SSL/TLS certificado (Let's Encrypt)
- [ ] Firewall configurado (UFW)

## Logging y monitoreo
- [x] Logging configurado (archivo + consola)
- [ ] Rotación de logs (logrotate)
- [ ] Monitoreo de errores (Sentry opcional)

## Performance
- [ ] Cache configurado (Redis/Memcached)
- [ ] Compresión habilitada (GZip)
- [ ] CDN para estáticos (opcional)

## CI/CD
- [x] GitHub Actions workflow creado
- [ ] Tests ejecutándose en CI
- [ ] Deploy automático configurado

## Variables de entorno requeridas en producción
```
DJANGO_SECRET_KEY=<key-segura>
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com
```

## Comandos de deployment

### Preparación local
```bash
python manage.py check --deploy
python manage.py test
python manage.py collectstatic --noinput
```

### En servidor (Ubuntu/Debian)
```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# Configurar PostgreSQL
sudo -u postgres createdb fayucaplace
sudo -u postgres createuser fayuca_user
sudo -u postgres psql -c "ALTER USER fayuca_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fayucaplace TO fayuca_user;"

# Clonar y configurar app
cd /home/ubuntu
git clone https://github.com/DeyvenUwU/Fayucaplace.git
cd Fayucaplace
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn psycopg2-binary

# Variables de entorno
export DJANGO_SECRET_KEY="tu-clave-segura"
export DEBUG=False
export ALLOWED_HOSTS="tu-dominio.com"
export DATABASE_URL="postgres://fayuca_user:secure_password@localhost:5432/fayucaplace"

# Migrar y colectar estáticos
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell < setup_permissions.py

# Configurar servicios
sudo cp fayucaplace.service /etc/systemd/system/
sudo cp nginx_fayuca.conf /etc/nginx/sites-available/fayucaplace
sudo ln -s /etc/nginx/sites-available/fayucaplace /etc/nginx/sites-enabled/
sudo systemctl daemon-reload
sudo systemctl start fayucaplace
sudo systemctl enable fayucaplace
sudo systemctl restart nginx
```

### Verificación
```bash
sudo systemctl status fayucaplace
sudo systemctl status nginx
curl http://localhost
```

## Ngrok (desarrollo/demo)
```bash
# Instalar ngrok
snap install ngrok

# Configurar authtoken
ngrok config add-authtoken <tu-token>

# Exponer puerto 8000
ngrok http 8000

# Actualizar ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS con URL de ngrok
```

## Plataformas cloud alternativas
- **Railway**: Deploy directo desde GitHub, PostgreSQL incluido
- **Render**: Free tier, auto-deploy
- **Heroku**: Classic option, requiere Procfile
- **DigitalOcean App Platform**: Droplets o App Platform
- **AWS/GCP/Azure**: Mayor control, más configuración

## Troubleshooting común
- **502 Bad Gateway**: Verificar que Gunicorn está corriendo
- **403 Forbidden**: Permisos de archivos estáticos
- **CSRF Failed**: Agregar dominio a CSRF_TRUSTED_ORIGINS
- **Static files 404**: Ejecutar collectstatic
- **Database connection**: Verificar DATABASE_URL y permisos PostgreSQL
