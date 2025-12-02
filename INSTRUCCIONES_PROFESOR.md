# 🎯 INSTRUCCIONES PARA EL PROFESOR
## Configuración de Fayucaplace en Producción

---

## 📋 CHECKLIST DE ENTREGA

### ✅ Requisitos Cumplidos

- [x] **Configuración de Servidor Web**
  - ✅ Gunicorn configurado (`gunicorn_config.py`)
  - ✅ Scripts de inicio automatizados
  - ✅ Configuración de producción en `settings.py`

- [x] **CI/CD con GitHub Actions**
  - ✅ Pipeline completo en `.github/workflows/django-ci.yml`
  - ✅ Tests automáticos
  - ✅ Análisis de seguridad (Bandit, Safety)
  - ✅ Verificación de calidad (flake8)
  - ✅ Build check

- [x] **URL de Publicación**
  - ✅ Configuración con ngrok
  - ✅ Scripts automatizados para ngrok
  - ✅ URL pública accesible desde cualquier lugar

- [x] **Operación Correcta en Producción**
  - ✅ Modo DEBUG=False
  - ✅ Secret keys seguras
  - ✅ CSRF y seguridad configurada
  - ✅ Admin funcional
  - ✅ Operaciones públicas funcionales
  - ✅ Archivos estáticos servidos correctamente

---

## 🚀 PASOS PARA PROBAR EL PROYECTO

### Paso 1: Verificar el Sistema
```powershell
# Abrir PowerShell en la carpeta del proyecto
cd C:\Users\alexo\OneDrive\Documentos\GitHub\Fayucaplace

# Verificar que todo esté instalado
.\check_system.ps1
```

**Resultado esperado:** 
- ✅ Python instalado
- ✅ pip instalado
- ✅ Git instalado
- ✅ ngrok instalado (o instalar desde https://ngrok.com/download)

### Paso 2: Configurar ngrok (SOLO LA PRIMERA VEZ)
```powershell
# 1. Descargar ngrok desde: https://ngrok.com/download
# 2. Registrarse en ngrok: https://dashboard.ngrok.com/signup
# 3. Obtener authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
# 4. Configurar token:
ngrok config add-authtoken TU_TOKEN_AQUI
```

### Paso 3: Desplegar la Aplicación
```powershell
# Un solo comando para desplegar todo
.\deploy.ps1
```

**Esto hará automáticamente:**
1. ✅ Instalar dependencias
2. ✅ Aplicar migraciones
3. ✅ Recolectar archivos estáticos
4. ✅ Crear usuario admin (usuario: admin, password: admin123)
5. ✅ Iniciar ngrok
6. ✅ Iniciar servidor Gunicorn
7. ✅ Mostrar URL pública

### Paso 4: Verificar Funcionalidad

Una vez iniciado, verás algo como:

```
================================================
         SERVIDOR EN EJECUCIÓN
================================================
  🌐 URL pública: https://abcd-1234.ngrok-free.app
  🔐 Admin: https://abcd-1234.ngrok-free.app/admin
  🏠 Local: http://localhost:8000
  📊 Ngrok panel: http://localhost:4040
================================================
```

**Pruebas a realizar:**

1. **Acceso Público** - Abre en cualquier navegador:
   - URL: La que muestra en "URL pública"
   - Deberías ver la página principal de Fayucaplace

2. **Panel de Admin** - Abre:
   - URL: La que muestra en "Admin"
   - Credenciales: admin / admin123
   - Verifica que puedas:
     - ✅ Iniciar sesión
     - ✅ Ver usuarios
     - ✅ Ver publicaciones
     - ✅ Crear/editar contenido

3. **Operaciones Públicas** - Como usuario no autenticado:
   - ✅ Ver listado de publicaciones
   - ✅ Ver detalles de publicaciones
   - ✅ Filtrar por categorías
   - ✅ Búsqueda

4. **Panel de ngrok** - Abre: http://localhost:4040
   - ✅ Ver peticiones en tiempo real
   - ✅ Ver tiempos de respuesta

---

## 🔗 URLs PARA EL PROFESOR

Después de ejecutar `.\deploy.ps1`, comparte estas URLs:

| Recurso | URL |
|---------|-----|
| **Sitio Principal** | `https://[tu-url].ngrok-free.app` |
| **Admin Django** | `https://[tu-url].ngrok-free.app/admin` |
| **API REST** | `https://[tu-url].ngrok-free.app/api/` |
| **Repositorio GitHub** | `https://github.com/DeyvenUwU/Fayucaplace` |
| **GitHub Actions** | `https://github.com/DeyvenUwU/Fayucaplace/actions` |

**Credenciales del Admin:**
- Usuario: `admin`
- Contraseña: `admin123`

---

## 🤖 VERIFICAR CI/CD (GitHub Actions)

### Cómo verificar que funciona:

1. **Ver el workflow:**
   - Ir a: https://github.com/DeyvenUwU/Fayucaplace/actions
   - Deberías ver el pipeline "Django CI/CD Pipeline"

2. **Trigger manual:**
   ```powershell
   # Hacer un cambio pequeño
   git add .
   git commit -m "test: verificar CI/CD"
   git push origin master
   ```

3. **Verificar que ejecuta:**
   - Tests en Python 3.11 y 3.12
   - Análisis de seguridad
   - Build check
   - Quality check

---

## 📊 DEMOSTRACIÓN DE CARACTERÍSTICAS

### 1. Ambiente de Producción
- **DEBUG=False**: Configurado en `.env.production`
- **Secret Key**: Única y segura
- **ALLOWED_HOSTS**: Configurado para ngrok
- **CSRF Protection**: Activo
- **Gunicorn**: Servidor WSGI en producción

### 2. CI/CD Pipeline
- Ejecuta automáticamente en cada push
- Ver en: `.github/workflows/django-ci.yml`
- Incluye:
  - ✅ Tests unitarios
  - ✅ Análisis de seguridad (Bandit)
  - ✅ Verificación de dependencias (Safety)
  - ✅ Quality check (flake8)
  - ✅ Build verification

### 3. Servidor Web
- **Gunicorn**: Servidor WSGI production-ready
- **Workers**: Configurados según CPU
- **Timeouts**: Configurados apropiadamente
- **Logging**: Configurado para producción

### 4. Ngrok (Publicación)
- URL pública HTTPS automática
- Panel de inspección en tiempo real
- Accesible desde cualquier lugar

---

## 📁 ARCHIVOS CLAVE PARA REVISIÓN

### Configuración de Producción
- `mysite/settings.py` - Configuración Django con soporte para producción
- `gunicorn_config.py` - Configuración de Gunicorn
- `.env.production.example` - Plantilla de variables de entorno
- `.gitignore` - Archivos excluidos de Git

### Scripts de Despliegue
- `deploy.ps1` - Script principal de despliegue
- `start_ngrok.ps1` - Inicia y configura ngrok
- `start_production.ps1` - Inicia servidor en producción
- `check_system.ps1` - Verifica prerequisitos

### CI/CD
- `.github/workflows/django-ci.yml` - Pipeline de CI/CD

### Documentación
- `QUICKSTART.md` - Guía de inicio rápido
- `PRODUCTION_DEPLOYMENT.md` - Guía completa de producción
- `SETUP_SUMMARY.md` - Resumen de configuración
- `COMMANDS_CHEATSHEET.md` - Comandos útiles
- `README.md` - Documentación principal

---

## 🧪 PRUEBAS A REALIZAR

### Pruebas Funcionales

1. **Acceso Público**
   ```
   1. Abrir URL de ngrok en navegador
   2. Verificar que carga la página principal
   3. Navegar por diferentes secciones
   4. Verificar que los estilos se carguen correctamente
   ```

2. **Panel de Administración**
   ```
   1. Ir a /admin
   2. Login con admin/admin123
   3. Crear una nueva publicación
   4. Subir una imagen
   5. Editar la publicación
   6. Eliminar la publicación
   ```

3. **API REST**
   ```
   1. Abrir /api/
   2. Verificar endpoints disponibles
   3. Probar GET en /api/publicaciones/
   4. Verificar autenticación requerida para POST
   ```

4. **Operaciones de Usuario**
   ```
   1. Registrar nuevo usuario
   2. Iniciar sesión
   3. Crear publicación
   4. Ver perfil
   5. Editar perfil
   6. Cerrar sesión
   ```

### Pruebas de Seguridad

1. **DEBUG en False**
   ```powershell
   # Verificar en .env.production
   Get-Content .env.production | Select-String "DEBUG"
   # Debe mostrar: DEBUG=False
   ```

2. **HTTPS Activo**
   ```
   - URL de ngrok debe comenzar con https://
   - Verificar candado en navegador
   ```

3. **CSRF Protection**
   ```
   - Intentar POST sin token CSRF (debe fallar)
   - Verificar que formularios incluyen token CSRF
   ```

### Pruebas de CI/CD

1. **Verificar Pipeline**
   ```
   - Ir a GitHub Actions
   - Verificar último run
   - Todos los checks deben estar en verde
   ```

2. **Trigger Pipeline**
   ```powershell
   # Hacer un cambio y push
   git add .
   git commit -m "test: verificar pipeline"
   git push
   # Ir a GitHub Actions y ver que se ejecuta
   ```

---

## 📸 CAPTURAS RECOMENDADAS PARA ENTREGA

1. **Terminal mostrando el despliegue exitoso**
   - Comando: `.\deploy.ps1`
   - Salida mostrando URL pública

2. **Página principal del sitio**
   - URL pública de ngrok funcionando

3. **Panel de administración**
   - Login exitoso
   - Dashboard de admin

4. **Panel de ngrok**
   - http://localhost:4040
   - Mostrando peticiones

5. **GitHub Actions**
   - Pipeline ejecutándose con éxito
   - Todos los checks en verde

6. **Operación del negocio**
   - Crear publicación
   - Ver publicación
   - Editar perfil

---

## 🆘 SOLUCIÓN DE PROBLEMAS COMUNES

### "ngrok not found"
```powershell
# Solución 1: Instalar con Chocolatey
choco install ngrok

# Solución 2: Descargar manualmente
# Ir a https://ngrok.com/download
# Extraer ngrok.exe a C:\ngrok
# Agregar C:\ngrok al PATH
```

### "Port 8000 already in use"
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Matar el proceso (reemplaza 1234 con el PID real)
Stop-Process -Id 1234 -Force

# O usar otro puerto
.\deploy.ps1 -Port 8080
```

### "Database is locked"
```powershell
# Detener todos los procesos Python
Get-Process python | Stop-Process -Force

# Reiniciar
.\deploy.ps1
```

### "CSRF verification failed"
```powershell
# Verificar que NGROK_URL esté configurado
Get-Content .env.production | Select-String "NGROK_URL"

# Si no está, ejecutar:
.\start_ngrok.ps1  # Esto actualiza la URL
```

---

## 📞 INFORMACIÓN DE CONTACTO

**Estudiante:** Alex
**Proyecto:** Fayucaplace
**Repositorio:** https://github.com/DeyvenUwU/Fayucaplace
**Fecha:** Diciembre 2025

---

## ✅ LISTA DE VERIFICACIÓN FINAL

Antes de entregar, verificar:

- [ ] Proyecto desplegado con `.\deploy.ps1`
- [ ] URL pública de ngrok funcionando
- [ ] Admin accesible y funcional
- [ ] Operaciones públicas funcionando
- [ ] CI/CD ejecutándose en GitHub Actions
- [ ] Documentación completa en el repositorio
- [ ] README.md actualizado
- [ ] Credenciales de admin compartidas
- [ ] URL del sitio compartida
- [ ] Screenshots/evidencias preparadas

---

## 🎯 RESUMEN EJECUTIVO

### Lo que se entrega:

1. **Aplicación Django en Producción**
   - Servidor: Gunicorn
   - Configuración: Production-ready (DEBUG=False)
   - Seguridad: CSRF, XSS, HTTPS

2. **CI/CD Completamente Configurado**
   - GitHub Actions
   - Tests automáticos
   - Análisis de seguridad
   - Quality checks

3. **URL Pública Funcional**
   - ngrok para acceso público
   - HTTPS habilitado
   - Accesible desde cualquier lugar

4. **Documentación Completa**
   - Guías de inicio rápido
   - Documentación detallada
   - Scripts automatizados
   - Troubleshooting

### Comandos para el profesor:

```powershell
# 1. Verificar sistema
.\check_system.ps1

# 2. Desplegar aplicación
.\deploy.ps1

# 3. Acceder al sitio
# Usar la URL que aparece en la terminal
```

**¡Eso es todo!** El proyecto está listo para ser evaluado.

---

**Última actualización:** Diciembre 2025
