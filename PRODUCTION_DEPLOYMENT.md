# 🚀 Guía de Despliegue en Producción - Fayucaplace

## 📋 Índice
1. [Prerequisitos](#prerequisitos)
2. [Instalación de ngrok](#instalación-de-ngrok)
3. [Configuración Inicial](#configuración-inicial)
4. [Despliegue Rápido](#despliegue-rápido)
5. [Despliegue Manual](#despliegue-manual)
6. [CI/CD con GitHub Actions](#cicd-con-github-actions)
7. [Solución de Problemas](#solución-de-problemas)
8. [Comandos Útiles](#comandos-útiles)

---

## 📦 Prerequisitos

### Software Requerido
- **Python 3.11+** 
- **pip** (gestor de paquetes de Python)
- **Git**
- **ngrok** (para exponer tu servidor local)
- **PowerShell** (viene con Windows)

### Verificar Instalaciones
```powershell
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar Git
git --version

# Verificar ngrok (después de instalarlo)
ngrok --version
```

---

## 🌐 Instalación de ngrok

### Opción 1: Descarga Directa
1. Ve a [https://ngrok.com/download](https://ngrok.com/download)
2. Descarga la versión para Windows
3. Extrae el archivo `ngrok.exe` a una carpeta (ej: `C:\ngrok\`)
4. Agrega la carpeta al PATH de Windows:
   - Busca "variables de entorno" en Windows
   - Edita la variable PATH
   - Agrega la ruta donde está `ngrok.exe`

### Opción 2: Con Chocolatey
```powershell
choco install ngrok
```

### Opción 3: Con Scoop
```powershell
scoop install ngrok
```

### Autenticación de ngrok
```powershell
# Regístrate en https://ngrok.com y obtén tu authtoken
ngrok config add-authtoken TU_AUTH_TOKEN_AQUI
```

---

## ⚙️ Configuración Inicial

### 1. Clonar el Repositorio
```powershell
git clone https://github.com/DeyvenUwU/Fayucaplace.git
cd Fayucaplace
```

### 2. Crear Entorno Virtual
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 4. Generar Secret Key
```powershell
python generate_secret_key.py
```

### 5. Configurar Variables de Entorno
```powershell
# Copiar el archivo de ejemplo
Copy-Item .env.production.example .env.production

# Editar .env.production con tu editor favorito
notepad .env.production
```

Asegúrate de cambiar estos valores en `.env.production`:
```env
DEBUG=False
DJANGO_SECRET_KEY=tu-secret-key-generada-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,.ngrok-free.app,.ngrok.io
NGROK_URL=
GUNICORN_BIND=0.0.0.0:8000
GUNICORN_WORKERS=4
```

---

## 🚀 Despliegue Rápido

### Método 1: Script Automático (Recomendado)
```powershell
# Despliegue completo (setup + ngrok + servidor)
.\deploy.ps1

# Solo configuración inicial
.\deploy.ps1 -SetupOnly

# Solo iniciar ngrok
.\deploy.ps1 -NgrokOnly

# Solo iniciar servidor (si ngrok ya está corriendo)
.\deploy.ps1 -ServerOnly

# Usar puerto diferente
.\deploy.ps1 -Port 8080
```

### Método 2: Scripts Separados
```powershell
# Terminal 1: Iniciar ngrok
.\start_ngrok.ps1

# Terminal 2: Iniciar servidor (en otra terminal)
.\start_production.ps1
```

### ✅ Verificar Despliegue
Una vez iniciado, verás algo como:
```
================================================
         SERVIDOR EN EJECUCIÓN
================================================
  🌐 URL pública: https://xxxx-xxxx.ngrok-free.app
  🔐 Admin: https://xxxx-xxxx.ngrok-free.app/admin
  🏠 Local: http://localhost:8000
  📊 Ngrok panel: http://localhost:4040
================================================
```

---

## 🔧 Despliegue Manual

Si prefieres hacer todo paso a paso:

### 1. Preparar Base de Datos
```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 2. Recolectar Archivos Estáticos
```powershell
python manage.py collectstatic --no-input --clear
```

### 3. Crear Superusuario
```powershell
python manage.py createsuperuser
```

### 4. Iniciar ngrok
```powershell
# En una terminal separada
ngrok http 8000
```

Copia la URL HTTPS que aparece (ej: `https://xxxx-xxxx.ngrok-free.app`)

### 5. Actualizar Variables de Entorno
Edita `.env.production` y agrega la URL de ngrok:
```env
NGROK_URL=https://xxxx-xxxx.ngrok-free.app
```

### 6. Iniciar Gunicorn
```powershell
# Cargar variables de entorno
Get-Content .env.production | ForEach-Object {
    if ($_ -match '^([^#].+?)=(.+)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "env:$name" -Value $value
    }
}

# Iniciar servidor
gunicorn mysite.wsgi:application --config gunicorn_config.py
```

---

## 🔄 CI/CD con GitHub Actions

El proyecto incluye un workflow de CI/CD que se ejecuta automáticamente en cada push.

### Configuración del Workflow

El archivo `.github/workflows/django-ci.yml` incluye:

1. **Tests Automatizados**: Ejecuta pruebas en Python 3.11 y 3.12
2. **Análisis de Seguridad**: Escaneo con Bandit y Safety
3. **Build Check**: Verifica la recolección de estáticos
4. **Quality Check**: Análisis de código con flake8

### Visualizar Resultados

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Verás el estado de cada workflow

### Badges de Estado

Agrega esto a tu `README.md`:
```markdown
![Django CI](https://github.com/DeyvenUwU/Fayucaplace/workflows/Django%20CI%2FCD%20Pipeline/badge.svg)
```

---

## 🐛 Solución de Problemas

### Error: "ngrok not found"
```powershell
# Verificar que ngrok esté en el PATH
$env:Path

# Si no está, agregarlo temporalmente
$env:Path += ";C:\ruta\a\ngrok"

# O instalarlo con chocolatey
choco install ngrok
```

### Error: "Port already in use"
```powershell
# Ver qué proceso usa el puerto 8000
netstat -ano | findstr :8000

# Matar el proceso (reemplaza PID con el número que aparece)
Stop-Process -Id PID -Force

# O usar otro puerto
.\deploy.ps1 -Port 8080
```

### Error: "Database is locked"
```powershell
# Detener todos los procesos de Django
Get-Process python | Stop-Process -Force

# Verificar que no haya procesos corriendo
python check_database.py
```

### Error: CSRF Verification Failed
```powershell
# Asegúrate de que la URL de ngrok esté en .env.production
# Reinicia el servidor después de actualizar
```

### Error: Static files not found
```powershell
# Recolectar archivos estáticos nuevamente
python manage.py collectstatic --no-input --clear

# Verificar la configuración en settings.py
python manage.py findstatic style.css
```

### Ngrok muestra "Visit Site" button
Esto es normal en la versión gratuita. Los visitantes deben clickear el botón para continuar.

---

## 📝 Comandos Útiles

### Gestión del Servidor
```powershell
# Ver logs de Gunicorn (si están en archivo)
Get-Content gunicorn.log -Tail 50

# Ver procesos de Python corriendo
Get-Process python

# Detener todos los procesos de Python
Get-Process python | Stop-Process -Force

# Ver procesos de ngrok
Get-Process ngrok

# Detener ngrok
if (Test-Path .ngrok.pid) {
    Stop-Process -Id (Get-Content .ngrok.pid)
}
```

### Django Management
```powershell
# Activar entorno virtual primero
.\venv\Scripts\Activate.ps1

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Verificar configuración
python manage.py check

# Ver URLs disponibles
python manage.py show_urls  # Si tienes django-extensions
```

### Base de Datos
```powershell
# Backup de la base de datos
Copy-Item db.sqlite3 "db.sqlite3.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Resetear base de datos (CUIDADO: Borra todos los datos)
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Git
```powershell
# Ver estado
git status

# Agregar cambios
git add .

# Commit
git commit -m "Descripción del cambio"

# Push
git push origin master

# Pull
git pull origin master
```

---

## 🔐 Seguridad en Producción

### Checklist de Seguridad

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` único y seguro (no usar el de desarrollo)
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] `CSRF_TRUSTED_ORIGINS` incluye tu dominio de ngrok
- [ ] Contraseña del admin cambiada después del primer login
- [ ] Base de datos con permisos correctos
- [ ] No subir `.env.production` a Git (está en .gitignore)
- [ ] SSL/HTTPS habilitado (ngrok lo proporciona automáticamente)

### Cambiar Contraseña de Admin
```powershell
python manage.py changepassword admin
```

---

## 📊 Monitoreo

### Panel de ngrok
Accede a `http://localhost:4040` para ver:
- Peticiones en tiempo real
- Tiempos de respuesta
- Errores
- Headers de peticiones

### Logs de Django
```powershell
# Si configuraste logging en settings.py
Get-Content django.log -Tail 100 -Wait
```

### Rendimiento
```powershell
# Ver uso de CPU y memoria
Get-Process python | Format-Table Id, CPU, WorkingSet, ProcessName
```

---

## 🎯 Flujo de Trabajo Recomendado

### Desarrollo Local
```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Hacer cambios en el código

# 3. Probar localmente
python manage.py runserver

# 4. Hacer commit
git add .
git commit -m "Descripción"
git push
```

### Despliegue a Producción
```powershell
# 1. Pull de los últimos cambios
git pull origin master

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Actualizar dependencias (si cambiaron)
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Recolectar estáticos
python manage.py collectstatic --no-input

# 6. Reiniciar servidor
.\deploy.ps1
```

---

## 📚 Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de Gunicorn](https://docs.gunicorn.org/)
- [Documentación de ngrok](https://ngrok.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa la sección de [Solución de Problemas](#solución-de-problemas)
2. Verifica los logs en `http://localhost:4040` (panel de ngrok)
3. Revisa los issues en GitHub
4. Contacta al administrador del proyecto

---

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE del repositorio.

---

**Última actualización**: Diciembre 2025
