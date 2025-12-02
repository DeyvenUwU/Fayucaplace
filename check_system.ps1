# Script de verificación del sistema para Fayucaplace

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DEL SISTEMA - FAYUCAPLACE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$allChecks = @()

function Test-Command($command) {
    try {
        Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# 1. Verificar Python
Write-Host "🐍 Verificando Python..." -NoNewline
if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Versión: $pythonVersion" -ForegroundColor Gray
    $allChecks += @{Name="Python"; Status="OK"; Details=$pythonVersion}
} else {
    Write-Host " ❌" -ForegroundColor Red
    Write-Host "   Python no está instalado" -ForegroundColor Red
    $allChecks += @{Name="Python"; Status="FAIL"; Details="No instalado"}
}

# 2. Verificar pip
Write-Host "📦 Verificando pip..." -NoNewline
if (Test-Command pip) {
    $pipVersion = pip --version 2>&1
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Versión: $pipVersion" -ForegroundColor Gray
    $allChecks += @{Name="pip"; Status="OK"; Details=$pipVersion}
} else {
    Write-Host " ❌" -ForegroundColor Red
    $allChecks += @{Name="pip"; Status="FAIL"; Details="No instalado"}
}

# 3. Verificar Git
Write-Host "📚 Verificando Git..." -NoNewline
if (Test-Command git) {
    $gitVersion = git --version 2>&1
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Versión: $gitVersion" -ForegroundColor Gray
    $allChecks += @{Name="Git"; Status="OK"; Details=$gitVersion}
} else {
    Write-Host " ❌" -ForegroundColor Red
    $allChecks += @{Name="Git"; Status="FAIL"; Details="No instalado"}
}

# 4. Verificar ngrok
Write-Host "🌐 Verificando ngrok..." -NoNewline
if (Test-Command ngrok) {
    $ngrokVersion = ngrok version 2>&1
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Versión: $ngrokVersion" -ForegroundColor Gray
    $allChecks += @{Name="ngrok"; Status="OK"; Details=$ngrokVersion}
} else {
    Write-Host " ⚠️" -ForegroundColor Yellow
    Write-Host "   ngrok no está instalado (opcional pero recomendado)" -ForegroundColor Yellow
    $allChecks += @{Name="ngrok"; Status="WARNING"; Details="No instalado"}
}

Write-Host ""
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DE ARCHIVOS DEL PROYECTO" -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host ""

# 5. Verificar archivos del proyecto
$requiredFiles = @(
    @{Path="manage.py"; Name="Django manage.py"},
    @{Path="requirements.txt"; Name="Requirements"},
    @{Path="gunicorn_config.py"; Name="Gunicorn config"},
    @{Path="mysite\settings.py"; Name="Django settings"},
    @{Path="deploy.ps1"; Name="Script de despliegue"},
    @{Path="start_ngrok.ps1"; Name="Script de ngrok"},
    @{Path="start_production.ps1"; Name="Script de producción"}
)

foreach ($file in $requiredFiles) {
    Write-Host "📄 Verificando $($file.Name)..." -NoNewline
    if (Test-Path $file.Path) {
        Write-Host " ✅" -ForegroundColor Green
        $allChecks += @{Name=$file.Name; Status="OK"; Details="Encontrado"}
    } else {
        Write-Host " ❌" -ForegroundColor Red
        $allChecks += @{Name=$file.Name; Status="FAIL"; Details="No encontrado"}
    }
}

Write-Host ""
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DE ENTORNO VIRTUAL" -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host ""

# 6. Verificar entorno virtual
Write-Host "🐍 Verificando entorno virtual..." -NoNewline
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Ubicación: venv\" -ForegroundColor Gray
    $allChecks += @{Name="Entorno Virtual"; Status="OK"; Details="venv\"}
} elseif (Test-Path "venv.venvScriptsactivate\bin\activate") {
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Ubicación: venv.venvScriptsactivate\" -ForegroundColor Gray
    $allChecks += @{Name="Entorno Virtual"; Status="OK"; Details="venv.venvScriptsactivate\"}
} else {
    Write-Host " ⚠️" -ForegroundColor Yellow
    Write-Host "   No se encontró entorno virtual. Créalo con: python -m venv venv" -ForegroundColor Yellow
    $allChecks += @{Name="Entorno Virtual"; Status="WARNING"; Details="No encontrado"}
}

Write-Host ""
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DE DEPENDENCIAS" -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host ""

# 7. Verificar dependencias de Python (si hay entorno virtual)
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "📦 Verificando dependencias instaladas..." -ForegroundColor Cyan
    
    # Activar entorno virtual temporalmente
    & "venv\Scripts\Activate.ps1"
    
    $requiredPackages = @("Django", "djangorestframework", "gunicorn", "Pillow")
    foreach ($package in $requiredPackages) {
        Write-Host "   $package..." -NoNewline
        $installed = pip show $package 2>&1
        if ($installed -match "Name: $package") {
            Write-Host " ✅" -ForegroundColor Green
        } else {
            Write-Host " ❌" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DE BASE DE DATOS" -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host ""

# 8. Verificar base de datos
Write-Host "🗄️  Verificando base de datos..." -NoNewline
if (Test-Path "db.sqlite3") {
    $dbSize = (Get-Item "db.sqlite3").Length / 1KB
    Write-Host " ✅" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($dbSize, 2)) KB" -ForegroundColor Gray
    $allChecks += @{Name="Base de datos"; Status="OK"; Details="$([math]::Round($dbSize, 2)) KB"}
} else {
    Write-Host " ⚠️" -ForegroundColor Yellow
    Write-Host "   Base de datos no existe. Se creará al ejecutar migraciones" -ForegroundColor Yellow
    $allChecks += @{Name="Base de datos"; Status="WARNING"; Details="No existe"}
}

Write-Host ""
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host "  VERIFICACIÓN DE CONFIGURACIÓN" -ForegroundColor Green
Write-Host "------------------------------------------------" -ForegroundColor Cyan
Write-Host ""

# 9. Verificar archivo de configuración de producción
Write-Host "⚙️  Verificando configuración de producción..." -NoNewline
if (Test-Path ".env.production") {
    Write-Host " ✅" -ForegroundColor Green
    
    # Verificar contenido
    $envContent = Get-Content ".env.production"
    $hasSecretKey = $envContent | Where-Object { $_ -match "^DJANGO_SECRET_KEY=" }
    $hasDebugFalse = $envContent | Where-Object { $_ -match "^DEBUG=False" }
    
    if ($hasSecretKey) {
        Write-Host "   SECRET_KEY configurada: ✅" -ForegroundColor Green
    } else {
        Write-Host "   SECRET_KEY configurada: ⚠️  (no encontrada)" -ForegroundColor Yellow
    }
    
    if ($hasDebugFalse) {
        Write-Host "   DEBUG=False: ✅" -ForegroundColor Green
    } else {
        Write-Host "   DEBUG=False: ⚠️  (verifica la configuración)" -ForegroundColor Yellow
    }
    
    $allChecks += @{Name="Config Producción"; Status="OK"; Details="Encontrado"}
} else {
    Write-Host " ⚠️" -ForegroundColor Yellow
    Write-Host "   Archivo .env.production no existe. Se creará al ejecutar deploy.ps1" -ForegroundColor Yellow
    $allChecks += @{Name="Config Producción"; Status="WARNING"; Details="No existe"}
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE VERIFICACIÓN" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$okCount = ($allChecks | Where-Object { $_.Status -eq "OK" }).Count
$warningCount = ($allChecks | Where-Object { $_.Status -eq "WARNING" }).Count
$failCount = ($allChecks | Where-Object { $_.Status -eq "FAIL" }).Count
$totalCount = $allChecks.Count

Write-Host "Total de verificaciones: $totalCount" -ForegroundColor White
Write-Host "✅ Exitosas: $okCount" -ForegroundColor Green
Write-Host "⚠️  Advertencias: $warningCount" -ForegroundColor Yellow
Write-Host "❌ Fallidas: $failCount" -ForegroundColor Red
Write-Host ""

if ($failCount -eq 0 -and $warningCount -eq 0) {
    Write-Host "🎉 ¡Todo está perfecto! Estás listo para desplegar." -ForegroundColor Green
    Write-Host ""
    Write-Host "Ejecuta: .\deploy.ps1" -ForegroundColor Cyan
} elseif ($failCount -eq 0) {
    Write-Host "✨ El sistema está casi listo. Revisa las advertencias arriba." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Puedes continuar ejecutando: .\deploy.ps1" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Hay problemas que debes resolver antes de continuar." -ForegroundColor Red
    Write-Host ""
    Write-Host "Revisa los elementos marcados con ❌ arriba." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Guardar reporte en archivo
$reportPath = "system_check_report.txt"
$allChecks | ForEach-Object {
    "$($_.Name): $($_.Status) - $($_.Details)"
} | Out-File -FilePath $reportPath

Write-Host "📄 Reporte guardado en: $reportPath" -ForegroundColor Gray
Write-Host ""
