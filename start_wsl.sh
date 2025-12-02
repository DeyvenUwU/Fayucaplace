#!/bin/bash
# Script completo de inicio para WSL/Linux - Todo en uno

echo "🚀 Iniciando Fayucaplace..."
echo ""

# Verificar si tmux está instalado
if ! command -v tmux &> /dev/null; then
    echo "📦 Instalando tmux..."
    sudo apt-get update > /dev/null 2>&1
    sudo apt-get install -y tmux > /dev/null 2>&1
fi

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "📦 Instalando ngrok..."
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.amd64.tgz | sudo tar xvz -C /usr/local/bin
    echo "⚠️  Necesitas configurar tu authtoken de ngrok:"
    echo "   1. Regístrate en: https://dashboard.ngrok.com/signup"
    echo "   2. Obtén tu token en: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "   3. Ejecuta: ngrok config add-authtoken TU_TOKEN"
    exit 1
fi

# Setup inicial
./setup_wsl.sh

# Crear sesión de tmux
SESSION="fayucaplace"

# Matar sesión anterior si existe
tmux kill-session -t $SESSION 2>/dev/null

# Crear nueva sesión
tmux new-session -d -s $SESSION

# Ventana 1: ngrok
tmux rename-window -t $SESSION:0 'ngrok'
tmux send-keys -t $SESSION:0 'ngrok http 8000' C-m

# Esperar a que ngrok inicie
sleep 3

# Ventana 2: servidor
tmux new-window -t $SESSION:1 -n 'server'
tmux send-keys -t $SESSION:1 'source venv/bin/activate' C-m
tmux send-keys -t $SESSION:1 'export DEBUG=False' C-m
tmux send-keys -t $SESSION:1 'gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 4' C-m

# Obtener URL de ngrok
sleep 2
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | grep -o 'https://[^"]*' | head -1)

# Ventana 3: info
tmux new-window -t $SESSION:2 -n 'info'
tmux send-keys -t $SESSION:2 'clear' C-m
tmux send-keys -t $SESSION:2 "echo '================================================'" C-m
tmux send-keys -t $SESSION:2 "echo '  FAYUCAPLACE ESTÁ CORRIENDO'" C-m
tmux send-keys -t $SESSION:2 "echo '================================================'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '🌐 URL Pública: $NGROK_URL'" C-m
tmux send-keys -t $SESSION:2 "echo '🔐 Admin: $NGROK_URL/admin'" C-m
tmux send-keys -t $SESSION:2 "echo '🏠 Local: http://localhost:8000'" C-m
tmux send-keys -t $SESSION:2 "echo '📊 Panel ngrok: http://localhost:4040'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '👤 Usuario: admin'" C-m
tmux send-keys -t $SESSION:2 "echo '🔑 Password: admin123'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo '================================================'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo 'Usa Ctrl+B y luego números para cambiar ventanas:'" C-m
tmux send-keys -t $SESSION:2 "echo '  0 - ngrok'" C-m
tmux send-keys -t $SESSION:2 "echo '  1 - servidor'" C-m
tmux send-keys -t $SESSION:2 "echo '  2 - info (esta ventana)'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m
tmux send-keys -t $SESSION:2 "echo 'Para salir de tmux: Ctrl+B, luego D'" C-m
tmux send-keys -t $SESSION:2 "echo 'Para volver: tmux attach -t fayucaplace'" C-m
tmux send-keys -t $SESSION:2 "echo 'Para detener todo: ./stop.sh'" C-m
tmux send-keys -t $SESSION:2 "echo ''" C-m

# Mostrar info en consola también
echo ""
echo "================================================"
echo "  FAYUCAPLACE ESTÁ CORRIENDO"
echo "================================================"
echo ""
echo "🌐 URL Pública: $NGROK_URL"
echo "🔐 Admin: $NGROK_URL/admin"
echo "🏠 Local: http://localhost:8000"
echo "📊 Panel ngrok: http://localhost:4040"
echo ""
echo "👤 Usuario: admin"
echo "🔑 Password: admin123"
echo ""
echo "================================================"
echo ""
echo "✨ Usa: tmux attach -t fayucaplace"
echo "   Para ver las ventanas de ngrok y servidor"
echo ""

# Adjuntar a la sesión en la ventana de info
tmux select-window -t $SESSION:2
tmux attach-session -t $SESSION
