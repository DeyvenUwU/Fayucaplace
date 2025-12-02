# 🎯 Comandos Rápidos - Fayucaplace

## 📌 Comandos Esenciales

### Verificar Sistema
```powershell
.\check_system.ps1
```

### Despliegue Completo (Todo en Uno)
```powershell
.\deploy.ps1
```

### Despliegue Manual (2 Terminales)
```powershell
# Terminal 1: Ngrok
.\start_ngrok.ps1

# Terminal 2: Servidor
.\start_production.ps1
```

---

## 🔧 Comandos de Configuración

### Solo Setup (sin iniciar)
```powershell
.\deploy.ps1 -SetupOnly
```

### Solo Ngrok
```powershell
.\deploy.ps1 -NgrokOnly
```

### Solo Servidor
```powershell
.\deploy.ps1 -ServerOnly
```

### Usar Puerto Diferente
```powershell
.\deploy.ps1 -Port 8080
```

---

## 🐍 Entorno Virtual

### Crear Entorno Virtual
```powershell
python -m venv venv
```

### Activar Entorno Virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### Desactivar Entorno Virtual
```powershell
deactivate
```

### Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### Actualizar pip
```powershell
python -m pip install --upgrade pip
```

---

## 📦 Django Management

### Migraciones
```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver migraciones pendientes
python manage.py showmigrations

# Ver SQL de una migración
python manage.py sqlmigrate app_name migration_name
```

### Archivos Estáticos
```powershell
# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Recolectar y limpiar anteriores
python manage.py collectstatic --no-input --clear

# Encontrar un archivo estático
python manage.py findstatic style.css
```

### Usuario Admin
```powershell
# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña
python manage.py changepassword admin

# Cambiar contraseña desde shell
python manage.py shell
# >>> from django.contrib.auth import get_user_model
# >>> User = get_user_model()
# >>> user = User.objects.get(username='admin')
# >>> user.set_password('nueva_contraseña')
# >>> user.save()
```

### Shell y Scripts
```powershell
# Shell interactivo de Django
python manage.py shell

# Ejecutar script Python con Django
python manage.py shell < script.py

# Shell con IPython (si está instalado)
python manage.py shell -i ipython
```

### Otros Comandos Django
```powershell
# Verificar problemas
python manage.py check

# Verificar configuración de despliegue
python manage.py check --deploy

# Limpiar sesiones expiradas
python manage.py clearsessions

# Ver URLs disponibles
python manage.py show_urls  # Requiere django-extensions
```

---

## 🗄️ Base de Datos

### Backup Base de Datos
```powershell
# Backup simple
Copy-Item db.sqlite3 db.sqlite3.backup

# Backup con fecha
Copy-Item db.sqlite3 "db.sqlite3.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
```

### Restaurar Base de Datos
```powershell
Copy-Item db.sqlite3.backup db.sqlite3
```

### Resetear Base de Datos (CUIDADO)
```powershell
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Verificar Integridad
```powershell
python check_database.py
```

---

## 🌐 ngrok

### Iniciar ngrok
```powershell
# Puerto 8000
ngrok http 8000

# Puerto personalizado
ngrok http 8080

# Con subdominio (requiere cuenta Pro)
ngrok http 8000 --subdomain=mi-subdominio
```

### Configurar Token
```powershell
ngrok config add-authtoken TU_TOKEN_AQUI
```

### Ver configuración
```powershell
ngrok config check
```

### Panel Web de ngrok
```
http://localhost:4040
```

### Detener ngrok
```powershell
# Ctrl+C en la terminal de ngrok

# O buscar y matar el proceso
Get-Process ngrok | Stop-Process

# O usar el PID guardado
if (Test-Path .ngrok.pid) {
    Stop-Process -Id (Get-Content .ngrok.pid)
}
```

---

## 🔍 Diagnóstico y Logs

### Ver Procesos Python
```powershell
Get-Process python
```

### Ver Procesos en Puerto Específico
```powershell
netstat -ano | findstr :8000
```

### Matar Proceso por Puerto
```powershell
# Ver qué proceso usa el puerto
$port = 8000
$process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.OwningProcess -Force
}
```

### Matar Todos los Procesos Python
```powershell
Get-Process python | Stop-Process -Force
```

### Ver Logs de Gunicorn (si se guardan en archivo)
```powershell
# Ver últimas 50 líneas
Get-Content gunicorn.log -Tail 50

# Ver en tiempo real
Get-Content gunicorn.log -Tail 10 -Wait
```

### Ver Uso de Recursos
```powershell
Get-Process python | Format-Table Id, CPU, WorkingSet, ProcessName
```

---

## 📝 Git

### Estado y Cambios
```powershell
# Ver estado
git status

# Ver diferencias
git diff

# Ver log
git log --oneline -10
```

### Agregar y Commit
```powershell
# Agregar todo
git add .

# Agregar archivo específico
git add archivo.py

# Commit
git commit -m "Descripción del cambio"

# Agregar y commit en uno
git commit -am "Descripción"
```

### Push y Pull
```powershell
# Pull (traer cambios)
git pull origin master

# Push (enviar cambios)
git push origin master

# Push forzado (CUIDADO)
git push origin master --force
```

### Ramas
```powershell
# Ver ramas
git branch

# Crear rama
git branch nueva-rama

# Cambiar a rama
git checkout nueva-rama

# Crear y cambiar
git checkout -b nueva-rama

# Fusionar rama
git merge nombre-rama
```

### Deshacer Cambios
```powershell
# Deshacer cambios en archivo (no commiteado)
git checkout -- archivo.py

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer último commit (perder cambios)
git reset --hard HEAD~1
```

---

## 🧪 Testing

### Ejecutar Tests
```powershell
# Todos los tests
python manage.py test

# App específica
python manage.py test posting

# Test específico
python manage.py test posting.tests.PublicacionTestCase

# Con verbosidad
python manage.py test --verbosity=2

# Mantener base de datos de test
python manage.py test --keepdb
```

### Coverage (si está instalado)
```powershell
# Instalar coverage
pip install coverage

# Ejecutar con coverage
coverage run --source='.' manage.py test

# Ver reporte
coverage report

# Generar HTML
coverage html
# Abrir htmlcov/index.html
```

---

## 🔐 Seguridad

### Generar Secret Key
```powershell
python generate_secret_key.py
```

### Verificar Configuración de Seguridad
```powershell
python manage.py check --deploy
```

### Escaneo de Seguridad (si está instalado)
```powershell
# Instalar bandit
pip install bandit

# Escanear
bandit -r . -x ./venv
```

### Verificar Dependencias Vulnerables
```powershell
# Instalar safety
pip install safety

# Verificar
safety check
```

---

## 🛠️ Mantenimiento

### Limpiar Archivos Temporales
```powershell
# Limpiar cache de Python
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse

# Limpiar archivos .pyc
Get-ChildItem -Path . -Filter *.pyc -Recurse | Remove-Item -Force
```

### Actualizar Dependencias
```powershell
# Ver paquetes desactualizados
pip list --outdated

# Actualizar un paquete
pip install --upgrade nombre-paquete

# Actualizar todos (con pip-review)
pip install pip-review
pip-review --auto
```

### Regenerar requirements.txt
```powershell
pip freeze > requirements.txt
```

---

## 📊 Monitoreo en Producción

### Panel de ngrok
```
http://localhost:4040
```

### Ver Peticiones en Tiempo Real
```
# Panel de ngrok muestra:
- Peticiones HTTP
- Tiempos de respuesta
- Headers
- Errores
```

### Métricas de Sistema
```powershell
# CPU y Memoria
Get-Process python | Format-Table ProcessName, CPU, WS -AutoSize

# Espacio en disco
Get-PSDrive C
```

---

## 🚨 Comandos de Emergencia

### Detener Todo
```powershell
# Matar Python
Get-Process python | Stop-Process -Force

# Matar ngrok
Get-Process ngrok | Stop-Process -Force

# O simplemente
Ctrl+C  # en cada terminal
```

### Reinicio Completo
```powershell
# 1. Detener todo
Get-Process python,ngrok | Stop-Process -Force

# 2. Limpiar
Remove-Item .ngrok.pid -ErrorAction SilentlyContinue

# 3. Reiniciar
.\deploy.ps1
```

### Restaurar a Estado Limpio
```powershell
# 1. Backup de DB
Copy-Item db.sqlite3 db.sqlite3.backup

# 2. Limpiar
Remove-Item db.sqlite3
Remove-Item -Recurse static_collected

# 3. Reconfigurar
.\deploy.ps1 -SetupOnly
```

---

## 💡 Trucos y Tips

### Alias Útiles (agregar a tu perfil de PowerShell)
```powershell
# Editar: notepad $PROFILE

# Agregar alias
function activate { .\venv\Scripts\Activate.ps1 }
function runserver { python manage.py runserver }
function deploy { .\deploy.ps1 }
function check { .\check_system.ps1 }
function mig { python manage.py migrate }
function makemig { python manage.py makemigrations }
```

### Variables de Entorno Temporales
```powershell
# Para la sesión actual
$env:DEBUG = "False"
$env:DJANGO_SECRET_KEY = "mi-secret-key"

# Ver todas las variables de entorno
Get-ChildItem Env:
```

### Ejecutar en Segundo Plano (Windows)
```powershell
# Iniciar en nueva ventana
Start-Process powershell -ArgumentList "-Command", ".\start_ngrok.ps1"
```

---

## 📱 URLs de Acceso Rápido

Después de `.\deploy.ps1`:

| Servicio | URL |
|----------|-----|
| Sitio Público | `https://xxxx.ngrok-free.app` |
| Admin Django | `https://xxxx.ngrok-free.app/admin` |
| API REST | `https://xxxx.ngrok-free.app/api/` |
| Panel ngrok | `http://localhost:4040` |
| Local | `http://localhost:8000` |
| GitHub Actions | `https://github.com/DeyvenUwU/Fayucaplace/actions` |

---

## 🎯 Flujo de Trabajo Típico

### Día a Día - Desarrollo
```powershell
# 1. Activar entorno
.\venv\Scripts\Activate.ps1

# 2. Actualizar código
git pull

# 3. Instalar dependencias nuevas (si las hay)
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Trabajar en el código...

# 6. Probar localmente
python manage.py runserver

# 7. Commit y push
git add .
git commit -m "feat: nueva funcionalidad"
git push
```

### Día a Día - Producción
```powershell
# 1. Verificar sistema
.\check_system.ps1

# 2. Desplegar
.\deploy.ps1

# 3. Verificar que funcione
# Abrir https://tu-url.ngrok-free.app

# 4. Monitorear
# Abrir http://localhost:4040
```

---

**Guarda este archivo** como referencia rápida para comandos cotidianos!

---

## 📚 Documentación Relacionada

- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) - Guía completa
- [SETUP_SUMMARY.md](SETUP_SUMMARY.md) - Resumen de configuración
- [README.md](README.md) - Documentación principal

---

Última actualización: Diciembre 2025
