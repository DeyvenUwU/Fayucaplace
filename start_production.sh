#!/bin/bash
# Script para iniciar la aplicación en modo producción

echo "🚀 Iniciando Fayucaplace en modo PRODUCCIÓN..."

# Cargar variables de entorno
if [ -f .env.production ]; then
    echo "📝 Cargando variables de entorno desde .env.production"
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "⚠️  Advertencia: No se encontró .env.production, usando valores por defecto"
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
elif [ -d "venv.venvScriptsactivate" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv.venvScriptsactivate/bin/activate
fi

# Asegurar que DEBUG esté en False
export DEBUG=False

# Migraciones
echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "🎨 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Crear superusuario si no existe (opcional)
echo "👤 Verificando superusuario..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Creando superusuario por defecto...")
    User.objects.create_superuser('admin', 'admin@fayucaplace.com', 'admin123')
    print("✅ Superusuario creado: admin / admin123")
else:
    print("✅ Ya existe un superusuario")
EOF

# Iniciar Gunicorn
echo "🦄 Iniciando Gunicorn..."
gunicorn mysite.wsgi:application --config gunicorn_config.py
