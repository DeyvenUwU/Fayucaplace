# 🚀 DESPLIEGUE DESDE GITHUB - GUÍA COMPLETA

## 📋 Opciones de Despliegue

### ✅ OPCIÓN 1: Render.com (RECOMENDADO - GRATIS)
- Gratis para siempre
- URL permanente HTTPS
- Conecta directamente con GitHub
- Deploy automático en cada push
- **Tiempo: 10 minutos**

### ⚡ OPCIÓN 2: Railway.app (GRATIS)
- $5 de crédito mensual gratis
- Muy fácil de usar
- Deploy con un click

### 🚁 OPCIÓN 3: Fly.io (GRATIS)
- 3 apps gratis
- Más control
- Requiere CLI

---

# 🎯 MÉTODO 1: RENDER.COM (EL MÁS FÁCIL)

## Pasos Detallados

### PASO 1: Subir Cambios a GitHub

```bash
# Desde tu terminal (PowerShell o WSL)
cd C:\Users\alexo\OneDrive\Documentos\GitHub\Fayucaplace

# Agregar todos los archivos nuevos
git add .

# Hacer commit
git commit -m "feat: configuración para Render"

# Subir a GitHub
git push origin master
```

### PASO 2: Crear Cuenta en Render

1. Ve a: **https://render.com/**
2. Click en **"Get Started for Free"**
3. **Registrate con GitHub** (más fácil)
4. Autoriza a Render para acceder a tus repos

### PASO 3: Crear Web Service

1. En el Dashboard de Render, click en **"New +"**
2. Selecciona **"Web Service"**
3. Busca y selecciona tu repo: **`Fayucaplace`**
4. Click en **"Connect"**

### PASO 4: Configurar el Servicio

Usa estos valores EXACTOS:

#### Basic Settings
```
Name: fayucaplace
Region: Oregon (US West)
Branch: master
Root Directory: (dejar vacío)
Runtime: Python 3
```

#### Build & Deploy
```
Build Command:
chmod +x build.sh && ./build.sh

Start Command:
gunicorn mysite.wsgi:application
```

#### Environment Variables

Click en **"Add Environment Variable"** y agrega cada una:

1. **PYTHON_VERSION**
   - Value: `3.12.0`

2. **DEBUG**
   - Value: `False`

3. **DJANGO_SECRET_KEY**
   - Value: (genera uno nuevo con este comando en tu PC):
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **ALLOWED_HOSTS**
   - Value: `.onrender.com`

#### Instance Type
- Selecciona: **Free** (gratis)

### PASO 5: Deploy!

1. Click en **"Create Web Service"**
2. Render empezará a construir tu app (toma 2-3 minutos)
3. Verás los logs en tiempo real

### PASO 6: ¡Listo!

Tu sitio estará en:
```
https://fayucaplace.onrender.com
```

Admin:
```
https://fayucaplace.onrender.com/admin
Usuario: admin
Password: admin123
```

---

## 🗄️ OPCIONAL: Agregar Base de Datos PostgreSQL

### ¿Por qué?
- SQLite no funciona bien en servicios cloud
- PostgreSQL es gratis en Render
- Más robusto para producción

### Pasos:

1. En Render Dashboard, click **"New +"**
2. Selecciona **"PostgreSQL"**
3. Configuración:
   ```
   Name: fayucaplace-db
   Database: fayucaplace
   User: (autogenerado)
   Region: Oregon (US West) - mismo que tu app
   PostgreSQL Version: 15
   Datadog API Key: (dejar vacío)
   ```
4. Plan: **Free**
5. Click **"Create Database"**

6. Espera que se cree (1 minuto)

7. En la página de la base de datos, copia la **"Internal Database URL"**

8. Ve a tu Web Service > Environment
9. Click **"Add Environment Variable"**:
   - Key: `DATABASE_URL`
   - Value: (pega la URL que copiaste)

10. Click **"Save Changes"**

11. Render re-desplegará automáticamente

---

## 🔄 Deploy Automático

Cada vez que hagas push a GitHub:

```bash
# Hacer cambios en tu código
git add .
git commit -m "feat: nuevo cambio"
git push origin master

# Render detecta el push y redespliega automáticamente (30 segundos)
```

---

## 📊 Monitorear tu Aplicación

En el Dashboard de Render puedes:
- ✅ Ver logs en tiempo real
- ✅ Ver métricas de uso
- ✅ Ver historial de despliegues
- ✅ Acceder a la terminal (shell)

---

## 🆘 Solución de Problemas

### "Build Failed"
```
1. Revisa los logs en Render
2. Verifica que build.sh tenga permisos:
   - En tu PC: chmod +x build.sh
   - Git add, commit, push
```

### "Application failed to start"
```
1. Verifica el Start Command: gunicorn mysite.wsgi:application
2. Verifica que gunicorn esté en requirements.txt
3. Revisa los logs para ver el error exacto
```

### "Static files not loading"
```
1. Verifica que build.sh ejecute collectstatic
2. Asegúrate de que whitenoise esté en requirements.txt
3. Verifica STATIC_ROOT en settings.py
```

### "Database error"
```
1. Verifica que DATABASE_URL esté configurado
2. Asegúrate de que psycopg2-binary y dj-database-url estén en requirements.txt
3. Verifica que las migraciones se hayan ejecutado
```

---

## 💰 Limitaciones del Plan Gratuito

**Render Free Tier:**
- ⏰ Servicio se duerme después de 15 min sin uso
- 🕐 Primera carga después de dormir: ~30 segundos
- 💾 750 horas gratis al mes (más que suficiente)
- 🗄️ PostgreSQL: 1GB gratis
- 📊 90 días de retención de datos

**Para evitar que se duerma:**
- Usa un servicio de ping (cron-job.org)
- O considera el plan de pago ($7/mes)

---

## 🎓 Entregarle al Profesor

Comparte estos datos:

```
🌐 URL del Sitio: https://fayucaplace.onrender.com
🔐 Admin: https://fayucaplace.onrender.com/admin
👤 Usuario: admin
🔑 Password: admin123
📦 Repositorio: https://github.com/DeyvenUwU/Fayucaplace
🤖 CI/CD: https://github.com/DeyvenUwU/Fayucaplace/actions
📊 Dashboard Render: (tu panel de Render)
```

---

## ✅ Checklist de Entrega

- [ ] Código subido a GitHub
- [ ] Servicio creado en Render
- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL creada (opcional)
- [ ] Primer despliegue exitoso
- [ ] Sitio accesible públicamente
- [ ] Admin funcional
- [ ] CI/CD ejecutándose en GitHub Actions
- [ ] URLs compartidas con el profesor

---

## 🚀 RESUMEN ULTRA-RÁPIDO

```bash
# 1. Subir a GitHub
git add .
git commit -m "ready for deploy"
git push origin master

# 2. Ir a render.com y crear cuenta con GitHub

# 3. New + > Web Service > Conectar repo

# 4. Configurar:
Build: chmod +x build.sh && ./build.sh
Start: gunicorn mysite.wsgi:application

# 5. Agregar variables:
PYTHON_VERSION=3.12.0
DEBUG=False
DJANGO_SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=.onrender.com

# 6. Create Web Service

# 7. ¡Esperar 3 minutos y listo!
```

---

**¡Tu aplicación estará en línea 24/7 con URL permanente!** 🎉
