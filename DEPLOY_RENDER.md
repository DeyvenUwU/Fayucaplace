# Guía de Despliegue en Render.com (GRATIS)

## ¿Por qué Render?
- ✅ 100% Gratis
- ✅ HTTPS automático
- ✅ URL permanente (no cambia)
- ✅ Disponible 24/7
- ✅ Fácil de configurar
- ✅ Se conecta con GitHub

---

## 📋 Pasos para Desplegar en Render

### PASO 1: Preparar el Proyecto

Ya está listo, solo necesitamos asegurar algunos archivos:

### PASO 2: Crear Cuenta en Render

1. Ve a: https://render.com/
2. Click en "Get Started for Free"
3. Registrate con tu cuenta de GitHub (recomendado)

### PASO 3: Crear un Nuevo Web Service

1. En el dashboard de Render, click en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub: `DeyvenUwU/Fayucaplace`
4. Click en "Connect"

### PASO 4: Configurar el Servicio

En la configuración, usa estos valores:

**Basic Settings:**
- **Name:** `fayucaplace` (o el nombre que quieras)
- **Region:** Oregon (US West) o Frankfurt (Europe)
- **Branch:** `master`
- **Root Directory:** (dejar vacío)
- **Runtime:** Python 3

**Build & Deploy:**
- **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
  ```

- **Start Command:**
  ```bash
  gunicorn mysite.wsgi:application
  ```

**Environment Variables (Variables de Entorno):**

Click en "Advanced" y agrega estas variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.0` |
| `DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | `[genera una nueva con el script]` |
| `ALLOWED_HOSTS` | `[tu-app].onrender.com` |
| `DATABASE_URL` | (Render lo crea automáticamente si usas PostgreSQL) |

**Plan:**
- Selecciona el plan "Free" (gratis)

### PASO 5: Deploy!

1. Click en "Create Web Service"
2. Render automáticamente:
   - Clonará tu repositorio
   - Instalará las dependencias
   - Ejecutará las migraciones
   - Iniciará el servidor

3. Espera 2-3 minutos

4. Tu sitio estará disponible en:
   ```
   https://fayucaplace.onrender.com
   ```

---

## 🔑 Generar SECRET_KEY

Ejecuta esto localmente para generar una clave segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y úsalo en la variable `DJANGO_SECRET_KEY` en Render.

---

## 🗄️ Base de Datos (Opcional pero Recomendado)

Render ofrece PostgreSQL gratis:

1. En Render Dashboard, click en "New +"
2. Selecciona "PostgreSQL"
3. Configuración:
   - **Name:** fayucaplace-db
   - **Database:** fayucaplace
   - **User:** (autogenerado)
   - **Region:** Mismo que tu Web Service
   - **Plan:** Free

4. Click en "Create Database"

5. Una vez creada, copia la "Internal Database URL"

6. En tu Web Service, agrega la variable de entorno:
   - **Key:** `DATABASE_URL`
   - **Value:** (la URL que copiaste)

---

## 🔧 Configuración Automática con GitHub

### Despliegue Automático

Render se despliega automáticamente cuando haces push a GitHub:

```bash
# Hacer cambios en tu código
git add .
git commit -m "feat: nueva característica"
git push origin master

# Render detecta el push y redespliega automáticamente
```

---

## 📊 Monitoreo

En el Dashboard de Render puedes ver:
- ✅ Logs en tiempo real
- ✅ Estado del servicio
- ✅ Métricas de uso
- ✅ Historial de despliegues

---

## 🔗 URLs Finales

Después del despliegue:

- **Sitio:** `https://fayucaplace.onrender.com`
- **Admin:** `https://fayucaplace.onrender.com/admin`
- **API:** `https://fayucaplace.onrender.com/api/`

---

## ⚠️ Importante: Primera Vez

La primera vez que se despliega:

1. Espera a que el despliegue termine
2. Ve a los logs y busca errores
3. Crea un superusuario manualmente:

En Render, ve a tu servicio > Shell y ejecuta:
```bash
python manage.py createsuperuser
```

O agrega esto al Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@fayucaplace.com', 'admin123') if not User.objects.filter(username='admin').exists() else None"
```

---

## 💰 Limitaciones del Plan Gratuito

- ⏰ El servicio se duerme después de 15 min de inactividad
- 🕐 Primera carga después de dormir toma ~30 segundos
- 💾 750 horas gratis al mes (suficiente para un sitio personal)
- 📊 Base de datos PostgreSQL gratis con 1GB

**Nota:** Para producción real, considera el plan de pago ($7/mes)

---

## 🔄 Alternativas a Render

Si prefieres otra plataforma:

### Railway.app
- Similar a Render
- $5 de crédito gratis mensual
- Muy fácil de usar

### Fly.io
- Gratis para 3 apps pequeñas
- Más flexible
- Requiere más configuración

### PythonAnywhere
- Especializado en Python
- Plan gratis limitado
- Bueno para aprender

---

## 📚 Recursos

- [Documentación de Render](https://render.com/docs)
- [Django en Render](https://render.com/docs/deploy-django)
- [PostgreSQL en Render](https://render.com/docs/databases)

---

## 🆘 Problemas Comunes

### "Application failed to start"
- Revisa los logs en Render
- Verifica que `gunicorn` esté en `requirements.txt`
- Verifica las variables de entorno

### "Static files not loading"
- Asegúrate de ejecutar `collectstatic` en el Build Command
- Verifica `STATIC_ROOT` en settings.py

### "Database connection error"
- Verifica que `DATABASE_URL` esté configurado
- Asegúrate de tener `psycopg2-binary` en `requirements.txt`

---

## ✅ Checklist de Despliegue

- [ ] Cuenta en Render creada
- [ ] Repositorio conectado
- [ ] Build Command configurado
- [ ] Start Command configurado
- [ ] Variables de entorno configuradas
- [ ] Base de datos creada (opcional)
- [ ] Primer despliegue exitoso
- [ ] Superusuario creado
- [ ] Sitio accesible públicamente

---

**¡Listo para producción profesional!** 🚀
