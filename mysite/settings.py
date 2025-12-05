from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SECURITY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key')

# DEBUG: False en producción, True en desarrollo
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ✔ Permite ngrok, localhost y servicios cloud (Render, Railway, etc.)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,.ngrok-free.app,.ngrok.io,.onrender.com,.railway.app').split(',')

# ✔ Acepta CSRF desde ngrok y servicios cloud
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://*.ngrok-free.app',
    'https://*.ngrok-free.dev',
    'https://*.ngrok.io',
    'https://*.onrender.com',
    'https://*.railway.app',
    'https://*.fly.dev',
]

# Agregar URLs dinámicamente si existen
NGROK_URL = os.environ.get('NGROK_URL')
RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL')

for url in [NGROK_URL, RENDER_EXTERNAL_URL]:
    if url:
        if url not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(url)
        # Extraer el host de la URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if parsed.netloc and parsed.netloc not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(parsed.netloc)

# APLICACIONES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'profiles',
    'posting',
    'chat',

    'rest_framework',
    'rest_framework.authtoken',
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# ✔ Base de datos
# Soporta DATABASE_URL para servicios cloud (Render, Railway, etc.)
import dj_database_url

if os.environ.get('DATABASE_URL'):
    # Producción: usar PostgreSQL de Render/Railway
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desarrollo: usar SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# PASSWORD
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

# WhiteNoise configuration para servir archivos estáticos eficientemente
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Dominios desde los que se puede consumir la API
# Sustituye por el dominio real de tu frontend


#CORS_ALLOWED_ORIGINS = [
 #   "https://tudominio-frontend.com", #Tadan cambia la direccion por la direccion de dominio
    # "https://otro-dominio.com",
#]



if not DEBUG:
    # Cookies solo por HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Redirigir siempre a HTTPS
    SECURE_SSL_REDIRECT = True

    # HSTS: obliga a usar HTTPS por un año
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Protege contra algunos ataques de tipo MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Evita que el sitio sea embebido en iframes (clickjacking)
X_FRAME_OPTIONS = 'DENY'


