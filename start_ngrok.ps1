# Script para iniciar ngrok y configurar la URL automáticamente (PowerShell)

Write-Host "🌐 Iniciando ngrok..." -ForegroundColor Green

# Puerto donde corre Gunicorn
$Port = if ($args[0]) { $args[0] } else { 8000 }

# Verificar que ngrok está instalado
if (-not (Get-Command ngrok -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: ngrok no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Descarga ngrok desde: https://ngrok.com/download" -ForegroundColor Yellow
    exit 1
}

# Iniciar ngrok en segundo plano
Write-Host "🚀 Iniciando ngrok en el puerto $Port..." -ForegroundColor Cyan
$ngrokProcess = Start-Process -FilePath "ngrok" -ArgumentList "http", $Port -PassThru -WindowStyle Hidden

# Esperar a que ngrok inicie
Write-Host "⏳ Esperando a que ngrok inicie..." -ForegroundColor Cyan
Start-Sleep -Seconds 4

# Obtener la URL pública de ngrok
try {
    $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -Method Get
    $ngrokUrl = $response.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1 -ExpandProperty public_url
    
    if (-not $ngrokUrl) {
        throw "No se encontró una URL HTTPS en la respuesta de ngrok"
    }
} catch {
    Write-Host "❌ Error: No se pudo obtener la URL de ngrok" -ForegroundColor Red
    Write-Host "Detalles: $_" -ForegroundColor Red
    Write-Host "Asegúrate de que ngrok esté instalado y funcionando correctamente" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Ngrok iniciado exitosamente!" -ForegroundColor Green
Write-Host "🔗 URL pública: $ngrokUrl" -ForegroundColor Cyan

# Actualizar .env.production con la nueva URL
$envFile = ".env.production"
$envContent = @()

if (Test-Path $envFile) {
    # Leer el archivo existente y actualizar NGROK_URL
    $found = $false
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^NGROK_URL=') {
            $envContent += "NGROK_URL=$ngrokUrl"
            $found = $true
        } else {
            $envContent += $_
        }
    }
    
    # Si no se encontró NGROK_URL, agregarlo
    if (-not $found) {
        $envContent += "NGROK_URL=$ngrokUrl"
    }
    
    $envContent | Set-Content $envFile
    Write-Host "📝 Archivo .env.production actualizado" -ForegroundColor Cyan
} else {
    # Crear el archivo desde la plantilla
    if (Test-Path ".env.production.example") {
        Copy-Item ".env.production.example" $envFile
        # Actualizar NGROK_URL
        (Get-Content $envFile) -replace 'NGROK_URL=.*', "NGROK_URL=$ngrokUrl" | Set-Content $envFile
    } else {
        # Crear un archivo básico
        @"
DEBUG=False
DJANGO_SECRET_KEY=change-this-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,.ngrok-free.app,.ngrok.io
NGROK_URL=$ngrokUrl
GUNICORN_BIND=0.0.0.0:8000
GUNICORN_WORKERS=4
"@ | Set-Content $envFile
    }
    Write-Host "📝 Archivo .env.production creado" -ForegroundColor Cyan
}

# Exportar la variable para uso inmediato
$env:NGROK_URL = $ngrokUrl

Write-Host ""
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "  Fayucaplace está listo para producción" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "  URL pública: $ngrokUrl" -ForegroundColor Cyan
Write-Host "  Panel de ngrok: http://localhost:4040" -ForegroundColor Cyan
Write-Host "  Admin: $ngrokUrl/admin" -ForegroundColor Cyan
Write-Host "  PID de ngrok: $($ngrokProcess.Id)" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Ahora ejecuta en otra terminal: .\start_production.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para detener ngrok: Stop-Process -Id $($ngrokProcess.Id)" -ForegroundColor Gray
Write-Host ""

# Guardar el PID para referencia
$ngrokProcess.Id | Out-File -FilePath ".ngrok.pid" -NoNewline
