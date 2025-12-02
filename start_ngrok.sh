#!/bin/bash
# Script para iniciar ngrok y configurar la URL automáticamente

echo "🌐 Iniciando ngrok..."

# Puerto donde corre Gunicorn
PORT=${1:-8000}

# Iniciar ngrok en segundo plano y capturar la URL
ngrok http $PORT > /dev/null &
NGROK_PID=$!

# Esperar a que ngrok inicie
echo "⏳ Esperando a que ngrok inicie..."
sleep 3

# Obtener la URL pública de ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | grep -o 'https://[^"]*' | head -1)

if [ -z "$NGROK_URL" ]; then
    echo "❌ Error: No se pudo obtener la URL de ngrok"
    echo "Asegúrate de que ngrok esté instalado y funcionando correctamente"
    exit 1
fi

echo "✅ Ngrok iniciado exitosamente!"
echo "🔗 URL pública: $NGROK_URL"

# Actualizar .env.production con la nueva URL
if [ -f .env.production ]; then
    # Actualizar la línea NGROK_URL
    sed -i.bak "s|NGROK_URL=.*|NGROK_URL=$NGROK_URL|" .env.production
    echo "📝 Archivo .env.production actualizado"
else
    # Crear el archivo si no existe
    echo "NGROK_URL=$NGROK_URL" > .env.production
    echo "📝 Archivo .env.production creado"
fi

# Exportar la variable para uso inmediato
export NGROK_URL=$NGROK_URL

echo ""
echo "================================================"
echo "  Fayucaplace está listo para producción"
echo "================================================"
echo "  URL pública: $NGROK_URL"
echo "  Panel de ngrok: http://localhost:4040"
echo "  Admin: $NGROK_URL/admin"
echo "================================================"
echo ""
echo "💡 Ahora ejecuta: ./start_production.sh"
echo "   o en PowerShell: .\start_production.ps1"
echo ""
echo "Para detener ngrok: kill $NGROK_PID"
