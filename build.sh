#!/usr/bin/env bash
# Render.com build script

set -o errexit  # exit on error

echo "🔨 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input --clear

echo "🗄️ Aplicando migraciones..."
python manage.py migrate --no-input

echo "👤 Creando superusuario si no existe..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fayucaplace.com', 'admin123')
    print('✅ Superusuario creado: admin / admin123')
else:
    print('✅ Superusuario ya existe')
EOF

echo "✅ Build completado exitosamente!"
