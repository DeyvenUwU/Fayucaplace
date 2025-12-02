# Script completo de despliegue para Fayucaplace con ngrok (PowerShell)
# Este script maneja todo el proceso de despliegue en producción

param(
    [switch]$SetupOnly,
    [switch]$NgrokOnly,
    [switch]$ServerOnly,
    [string]$Port = "8000"
)

$ErrorActionPreference = "Stop"

function Write-ColorOutput($message, $color = "White") {
    Write-Host $message -ForegroundColor $color
}

function Show-Banner {
    Write-Host ""
    Write-ColorOutput "================================================" "Cyan"
    Write-ColorOutput "     FAYUCAPLACE - DESPLIEGUE EN PRODUCCIÓN    " "Green"
    Write-ColorOutput "================================================" "Cyan"
    Write-Host ""
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Verificando prerequisitos..." "Cyan"
    
    # Verificar Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-ColorOutput "❌ Error: Python no está instalado" "Red"
        exit 1
    }
    Write-ColorOutput "✅ Python encontrado" "Green"
    
    # Verificar ngrok
    if (-not (Get-Command ngrok -ErrorAction SilentlyContinue)) {
        Write-ColorOutput "⚠️  Advertencia: ngrok no está instalado" "Yellow"
        Write-ColorOutput "   Descarga desde: https://ngrok.com/download" "Yellow"
        $response = Read-Host "¿Deseas continuar sin ngrok? (y/n)"
        if ($response -ne "y") {
            exit 1
        }
    } else {
        Write-ColorOutput "✅ ngrok encontrado" "Green"
    }
    
    # Verificar archivos importantes
    $requiredFiles = @("manage.py", "requirements.txt", "gunicorn_config.py")
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-ColorOutput "❌ Error: No se encontró $file" "Red"
            exit 1
        }
    }
    Write-ColorOutput "✅ Archivos de proyecto encontrados" "Green"
    Write-Host ""
}

function Setup-Environment {
    Write-ColorOutput "🔧 Configurando entorno..." "Cyan"
    
    # Activar entorno virtual
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-ColorOutput "🐍 Activando entorno virtual..." "Cyan"
        & "venv\Scripts\Activate.ps1"
    }
    
    # Crear .env.production si no existe
    if (-not (Test-Path ".env.production")) {
        Write-ColorOutput "📝 Creando archivo .env.production..." "Cyan"
        if (Test-Path ".env.production.example") {
            Copy-Item ".env.production.example" ".env.production"
        } else {
            @"
DEBUG=False
DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALLOWED_HOSTS=localhost,127.0.0.1,.ngrok-free.app,.ngrok.io
NGROK_URL=
GUNICORN_BIND=0.0.0.0:$Port
GUNICORN_WORKERS=4
"@ | Set-Content ".env.production"
        }
        Write-ColorOutput "✅ Archivo .env.production creado" "Green"
    }
    
    # Cargar variables de entorno
    if (Test-Path ".env.production") {
        Get-Content ".env.production" | ForEach-Object {
            if ($_ -match '^([^#].+?)=(.+)$') {
                $name = $matches[1].Trim()
                $value = $matches[2].Trim()
                Set-Item -Path "env:$name" -Value $value
            }
        }
    }
    
    # Asegurar DEBUG=False
    $env:DEBUG = "False"
    
    Write-ColorOutput "✅ Entorno configurado" "Green"
    Write-Host ""
}

function Install-Dependencies {
    Write-ColorOutput "📦 Instalando dependencias..." "Cyan"
    
    python -m pip install --upgrade pip | Out-Null
    pip install -r requirements.txt | Out-Null
    
    Write-ColorOutput "✅ Dependencias instaladas" "Green"
    Write-Host ""
}

function Run-DatabaseMigrations {
    Write-ColorOutput "📦 Aplicando migraciones de base de datos..." "Cyan"
    
    python manage.py makemigrations --no-input
    python manage.py migrate --no-input
    
    Write-ColorOutput "✅ Migraciones aplicadas" "Green"
    Write-Host ""
}

function Collect-StaticFiles {
    Write-ColorOutput "🎨 Recolectando archivos estáticos..." "Cyan"
    
    python manage.py collectstatic --no-input --clear | Out-Null
    
    Write-ColorOutput "✅ Archivos estáticos recolectados" "Green"
    Write-Host ""
}

function Setup-Superuser {
    Write-ColorOutput "👤 Verificando superusuario..." "Cyan"
    
    $checkScript = @"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('CREATE')
else:
    print('EXISTS')
"@
    
    $result = python manage.py shell -c $checkScript
    
    if ($result -match "CREATE") {
        Write-ColorOutput "📝 Creando superusuario..." "Yellow"
        Write-ColorOutput "   Usuario: admin" "Gray"
        Write-ColorOutput "   Email: admin@fayucaplace.com" "Gray"
        Write-ColorOutput "   Contraseña: admin123" "Gray"
        
        $createScript = @"
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@fayucaplace.com', 'admin123')
print('Superusuario creado exitosamente')
"@
        python manage.py shell -c $createScript
        Write-ColorOutput "⚠️  IMPORTANTE: Cambia la contraseña después del primer login" "Yellow"
    } else {
        Write-ColorOutput "✅ Superusuario ya existe" "Green"
    }
    Write-Host ""
}

function Start-Ngrok {
    Write-ColorOutput "🌐 Iniciando ngrok en el puerto $Port..." "Cyan"
    
    # Iniciar ngrok
    $ngrokProcess = Start-Process -FilePath "ngrok" -ArgumentList "http", $Port -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 4
    
    # Obtener URL
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -Method Get
        $ngrokUrl = $response.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1 -ExpandProperty public_url
        
        if ($ngrokUrl) {
            # Actualizar .env.production
            $envContent = Get-Content ".env.production"
            $envContent = $envContent -replace 'NGROK_URL=.*', "NGROK_URL=$ngrokUrl"
            $envContent | Set-Content ".env.production"
            
            $env:NGROK_URL = $ngrokUrl
            
            Write-ColorOutput "✅ Ngrok iniciado exitosamente" "Green"
            Write-ColorOutput "🔗 URL pública: $ngrokUrl" "Cyan"
            Write-ColorOutput "📊 Panel de ngrok: http://localhost:4040" "Cyan"
            
            # Guardar PID
            $ngrokProcess.Id | Out-File -FilePath ".ngrok.pid" -NoNewline
            
            return $ngrokUrl
        }
    } catch {
        Write-ColorOutput "❌ Error al obtener URL de ngrok: $_" "Red"
        return $null
    }
    Write-Host ""
}

function Start-GunicornServer {
    Write-ColorOutput "🦄 Iniciando servidor Gunicorn..." "Green"
    Write-Host ""
    Write-ColorOutput "================================================" "Yellow"
    Write-ColorOutput "         SERVIDOR EN EJECUCIÓN" "Green"
    Write-ColorOutput "================================================" "Yellow"
    
    if ($env:NGROK_URL) {
        Write-ColorOutput "  🌐 URL pública: $($env:NGROK_URL)" "Cyan"
        Write-ColorOutput "  🔐 Admin: $($env:NGROK_URL)/admin" "Cyan"
    }
    Write-ColorOutput "  🏠 Local: http://localhost:$Port" "Cyan"
    Write-ColorOutput "  📊 Ngrok panel: http://localhost:4040" "Cyan"
    Write-ColorOutput "================================================" "Yellow"
    Write-Host ""
    Write-ColorOutput "Presiona Ctrl+C para detener el servidor" "Yellow"
    Write-Host ""
    
    # Iniciar Gunicorn
    gunicorn mysite.wsgi:application --config gunicorn_config.py
}

function Show-Help {
    Write-Host ""
    Write-Host "Uso: .\deploy.ps1 [opciones]"
    Write-Host ""
    Write-Host "Opciones:"
    Write-Host "  -SetupOnly    Solo configurar el entorno (no iniciar servidores)"
    Write-Host "  -NgrokOnly    Solo iniciar ngrok"
    Write-Host "  -ServerOnly   Solo iniciar el servidor (asume que ngrok ya está corriendo)"
    Write-Host "  -Port <port>  Especificar puerto (default: 8000)"
    Write-Host ""
    Write-Host "Ejemplos:"
    Write-Host "  .\deploy.ps1                 # Despliegue completo"
    Write-Host "  .\deploy.ps1 -SetupOnly      # Solo configuración"
    Write-Host "  .\deploy.ps1 -Port 8080      # Usar puerto 8080"
    Write-Host ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Show-Banner

# Si no hay parámetros, hacer despliegue completo
if (-not ($SetupOnly -or $NgrokOnly -or $ServerOnly)) {
    Test-Prerequisites
    Setup-Environment
    Install-Dependencies
    Run-DatabaseMigrations
    Collect-StaticFiles
    Setup-Superuser
    
    $ngrokUrl = Start-Ngrok
    
    if ($ngrokUrl) {
        Write-Host ""
        Write-ColorOutput "🎉 Setup completado exitosamente!" "Green"
        Write-Host ""
        Start-Sleep -Seconds 2
    }
    
    Start-GunicornServer
}
elseif ($SetupOnly) {
    Test-Prerequisites
    Setup-Environment
    Install-Dependencies
    Run-DatabaseMigrations
    Collect-StaticFiles
    Setup-Superuser
    
    Write-Host ""
    Write-ColorOutput "✅ Setup completado. Para iniciar el servidor ejecuta:" "Green"
    Write-ColorOutput "   .\deploy.ps1 -ServerOnly" "Cyan"
    Write-Host ""
}
elseif ($NgrokOnly) {
    $ngrokUrl = Start-Ngrok
    if ($ngrokUrl) {
        Write-Host ""
        Write-ColorOutput "✅ Ngrok iniciado. URL: $ngrokUrl" "Green"
        Write-ColorOutput "   Presiona Ctrl+C para detener" "Yellow"
        Write-Host ""
        
        # Mantener el script corriendo
        try {
            while ($true) {
                Start-Sleep -Seconds 1
            }
        } finally {
            Write-ColorOutput "Deteniendo ngrok..." "Yellow"
        }
    }
}
elseif ($ServerOnly) {
    Setup-Environment
    Start-GunicornServer
}
