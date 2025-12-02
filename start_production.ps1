# Script para iniciar la aplicación en modo producción (PowerShell)

Write-Host "🚀 Iniciando Fayucaplace en modo PRODUCCIÓN..." -ForegroundColor Green

# Cargar variables de entorno
if (Test-Path .env.production) {
    Write-Host "📝 Cargando variables de entorno desde .env.production" -ForegroundColor Cyan
    Get-Content .env.production | ForEach-Object {
        if ($_ -match '^([^#].+?)=(.+)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
} else {
    Write-Host "⚠️  Advertencia: No se encontró .env.production, usando valores por defecto" -ForegroundColor Yellow
}

# Activar entorno virtual si existe
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "🐍 Activando entorno virtual..." -ForegroundColor Cyan
    & "venv\Scripts\Activate.ps1"
} elseif (Test-Path "venv.venvScriptsactivate\bin\activate") {
    Write-Host "🐍 Activando entorno virtual..." -ForegroundColor Cyan
    & "venv.venvScriptsactivate\bin\activate"
}

# Asegurar que DEBUG esté en False
$env:DEBUG = "False"

# Migraciones
Write-Host "📦 Aplicando migraciones..." -ForegroundColor Cyan
python manage.py migrate --noinput

# Recolectar archivos estáticos
Write-Host "🎨 Recolectando archivos estáticos..." -ForegroundColor Cyan
python manage.py collectstatic --noinput --clear

# Crear superusuario si no existe (opcional)
Write-Host "👤 Verificando superusuario..." -ForegroundColor Cyan
python manage.py shell -c @"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creando superusuario por defecto...')
    User.objects.create_superuser('admin', 'admin@fayucaplace.com', 'admin123')
    print('✅ Superusuario creado: admin / admin123')
else:
    print('✅ Ya existe un superusuario')
"@

# Iniciar Gunicorn
Write-Host "🦄 Iniciando Gunicorn..." -ForegroundColor Green
gunicorn mysite.wsgi:application --config gunicorn_config.py
