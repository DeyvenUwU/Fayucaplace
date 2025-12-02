#!/bin/bash
# Script para detener todos los servicios

echo "🛑 Deteniendo Fayucaplace..."

# Matar sesión de tmux
tmux kill-session -t fayucaplace 2>/dev/null

# Matar procesos de Python
pkill -f gunicorn
pkill -f python

# Matar ngrok
pkill -f ngrok

echo "✅ Todos los servicios detenidos"
