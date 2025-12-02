#!/bin/bash
# Script simplificado para despliegue en WSL/Linux

echo "🚀 Iniciando Fayucaplace en WSL/Linux..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Error: No se encontró manage.py${NC}"
    echo "Asegúrate de estar en el directorio del proyecto"
    exit 1
fi

# Activar entorno virtual o crearlo
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

echo -e "${GREEN}🐍 Activando entorno virtual...${NC}"
source venv/bin/activate

# Instalar dependencias
echo -e "${GREEN}📦 Instalando dependencias...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Variables de entorno
export DEBUG=False
export DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null)

# Migraciones
echo -e "${GREEN}📦 Aplicando migraciones...${NC}"
python manage.py migrate --no-input

# Archivos estáticos
echo -e "${GREEN}🎨 Recolectando archivos estáticos...${NC}"
python manage.py collectstatic --no-input --clear > /dev/null 2>&1

# Crear superusuario si no existe
echo -e "${GREEN}👤 Verificando superusuario...${NC}"
python manage.py shell << EOF > /dev/null 2>&1
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@fayucaplace.com', 'admin123')
EOF

echo ""
echo -e "${GREEN}✅ Configuración completada${NC}"
echo ""
echo "================================================"
echo -e "${YELLOW}  SIGUIENTE PASO: Iniciar los servidores${NC}"
echo "================================================"
echo ""
echo "Abre 2 terminales y ejecuta:"
echo ""
echo -e "${YELLOW}Terminal 1:${NC}"
echo "  ngrok http 8000"
echo ""
echo -e "${YELLOW}Terminal 2:${NC}"
echo "  source venv/bin/activate"
echo "  gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 4"
echo ""
echo "O si prefieres, ejecuta:"
echo ""
echo -e "${YELLOW}Terminal 1:${NC} ./start_ngrok.sh"
echo -e "${YELLOW}Terminal 2:${NC} ./start_production.sh"
echo ""
echo "================================================"
echo -e "${GREEN}Credenciales Admin:${NC}"
echo "  Usuario: admin"
echo "  Password: admin123"
echo "================================================"
echo ""
