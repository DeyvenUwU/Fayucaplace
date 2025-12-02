# ⚡ Inicio Rápido - Fayucaplace en Producción

## 🎯 Despliegue en 3 Pasos

### Paso 1: Instalar ngrok
```powershell
# Descargar desde: https://ngrok.com/download
# Extraer ngrok.exe a C:\ngrok
# Agregar a PATH o usar ruta completa

# Autenticar (obtén tu token en https://dashboard.ngrok.com/get-started/your-authtoken)
ngrok config add-authtoken TU_TOKEN_AQUI
```

### Paso 2: Configurar el proyecto
```powershell
# Navegar al proyecto
cd C:\Users\alexo\OneDrive\Documentos\GitHub\Fayucaplace

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si no existe el entorno virtual, crearlo:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Paso 3: Desplegar
```powershell
# Ejecutar el script de despliegue
.\deploy.ps1
```

**¡Listo!** Tu aplicación estará corriendo y accesible públicamente vía ngrok.

---

## 📋 Lo que hace el script automáticamente

1. ✅ Verifica prerequisitos (Python, ngrok)
2. ✅ Configura variables de entorno
3. ✅ Instala dependencias de Python
4. ✅ Aplica migraciones de base de datos
5. ✅ Recolecta archivos estáticos
6. ✅ Crea superusuario (admin/admin123)
7. ✅ Inicia ngrok en puerto 8000
8. ✅ Inicia servidor Gunicorn
9. ✅ Muestra la URL pública

---

## 🔑 Credenciales por Defecto

**Usuario Admin:**
- Usuario: `admin`
- Email: `admin@fayucaplace.com`
- Contraseña: `admin123`

⚠️ **IMPORTANTE**: Cambia la contraseña después del primer login:
```powershell
python manage.py changepassword admin
```

---

## 🌐 URLs Importantes

Después de iniciar, tendrás acceso a:

- **Sitio Público**: `https://xxxx-xxxx.ngrok-free.app`
- **Panel Admin**: `https://xxxx-xxxx.ngrok-free.app/admin`
- **Panel ngrok**: `http://localhost:4040`
- **Local**: `http://localhost:8000`

---

## 🛠️ Comandos Alternativos

### Despliegue Manual (2 terminales)
```powershell
# Terminal 1: Iniciar ngrok
.\start_ngrok.ps1

# Terminal 2: Iniciar servidor
.\start_production.ps1
```

### Solo Configuración (sin iniciar)
```powershell
.\deploy.ps1 -SetupOnly
```

### Reiniciar Solo el Servidor
```powershell
.\deploy.ps1 -ServerOnly
```

---

## 🚨 Solución Rápida de Problemas

### "ngrok not found"
```powershell
# Opción 1: Instalar con Chocolatey
choco install ngrok

# Opción 2: Agregar a PATH temporalmente
$env:Path += ";C:\ngrok"
```

### "Port 8000 already in use"
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Matar el proceso
Stop-Process -Id PID -Force

# O usar otro puerto
.\deploy.ps1 -Port 8080
```

### "Database is locked"
```powershell
# Detener todos los procesos Python
Get-Process python | Stop-Process -Force
```

---

## 📊 Verificar que Todo Funciona

### 1. Verificar Ngrok
- Abre: `http://localhost:4040`
- Deberías ver el panel de ngrok con estadísticas

### 2. Verificar Sitio
- Abre la URL de ngrok que aparece en la consola
- Deberías ver la página principal de Fayucaplace

### 3. Verificar Admin
- Ve a: `https://tu-url-ngrok/admin`
- Login con: `admin` / `admin123`
- Deberías ver el panel de administración de Django

---

## 🔄 Actualizar Código

Cuando hagas cambios en el código:

```powershell
# 1. Pull de los cambios
git pull origin master

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Actualizar dependencias (si cambiaron)
pip install -r requirements.txt

# 4. Aplicar migraciones (si hay nuevas)
python manage.py migrate

# 5. Recolectar estáticos (si cambiaron)
python manage.py collectstatic --no-input

# 6. Reiniciar servidor
# Presiona Ctrl+C en la terminal del servidor
# Luego ejecuta nuevamente:
.\deploy.ps1 -ServerOnly
```

---

## 📱 Compartir tu Sitio

La URL de ngrok es **pública y accesible desde cualquier lugar**:

1. Copia la URL que aparece en la consola
2. Compártela con quien quieras
3. En la versión gratuita, los visitantes verán un botón "Visit Site" - solo deben hacer clic

**Nota**: La URL de ngrok cambia cada vez que reinicias ngrok. Para URLs permanentes, necesitas una cuenta de pago de ngrok o usar un servicio de hosting real.

---

## 🎓 GitHub Actions (CI/CD)

El proyecto ya tiene configurado CI/CD. Cada vez que hagas push a GitHub:

1. Se ejecutan las pruebas automáticamente
2. Se verifica la seguridad del código
3. Se comprueba que todo compile correctamente

Ver el estado en: `https://github.com/DeyvenUwU/Fayucaplace/actions`

---

## 📚 Más Información

Para detalles completos, consulta: [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)

---

## 🆘 ¿Necesitas Ayuda?

1. Revisa [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) - Guía completa
2. Verifica el panel de ngrok en `http://localhost:4040`
3. Revisa los logs en la consola
4. Consulta los issues en GitHub

---

**¡Feliz despliegue! 🚀**
