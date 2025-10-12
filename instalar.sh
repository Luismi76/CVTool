#!/bin/bash

# Script de instalación para CV Generator (Linux/macOS)

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${BLUE}  📄 CV GENERATOR - Instalación Automática${NC}"
echo -e "${BLUE}============================================================${NC}\n"

echo "Este script instalará CV Generator automáticamente."
echo ""
read -p "Presiona Enter para continuar..."

# Función para mostrar errores
error_exit() {
    echo -e "\n${RED}❌ ERROR: $1${NC}\n"
    exit 1
}

# Verificar Python
echo -e "\n${YELLOW}[1/5] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    error_exit "Python3 no está instalado. Instálalo con: sudo apt install python3 (Ubuntu/Debian) o brew install python3 (macOS)"
fi
echo -e "${GREEN}✅ Python encontrado: $(python3 --version)${NC}"

# Crear entorno virtual
echo -e "\n${YELLOW}[2/5] Creando entorno virtual...${NC}"
if [ -d "cv_env" ]; then
    echo -e "${YELLOW}⚠️  El entorno virtual ya existe. Eliminando...${NC}"
    rm -rf cv_env
fi
python3 -m venv cv_env || error_exit "No se pudo crear el entorno virtual"
echo -e "${GREEN}✅ Entorno virtual creado${NC}"

# Activar entorno virtual
echo -e "\n${YELLOW}[3/5] Activando entorno virtual...${NC}"
source cv_env/bin/activate || error_exit "No se pudo activar el entorno virtual"
echo -e "${GREEN}✅ Entorno virtual activado${NC}"

# Actualizar pip
echo -e "\n${YELLOW}[4/5] Instalando dependencias...${NC}"
python -m pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt || error_exit "No se pudieron instalar las dependencias"
echo -e "${GREEN}✅ Dependencias instaladas${NC}"

# Crear archivo .env
echo -e "\n${YELLOW}[5/5] Creando archivo de configuración...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Archivo .env creado${NC}"
    else
        echo -e "${YELLOW}⚠️  No se encontró .env.example${NC}"
    fi
else
    echo -e "${BLUE}ℹ️  Archivo .env ya existe${NC}"
fi

# Dar permisos de ejecución
chmod +x ejecutar.sh 2>/dev/null || true
chmod +x run.py 2>/dev/null || true

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${GREEN}  🎉 ¡Instalación completada con éxito!${NC}"
echo -e "${BLUE}============================================================${NC}\n"

echo "Para ejecutar la aplicación:"
echo "  ./ejecutar.sh"
echo ""
echo "O manualmente:"
echo "  source cv_env/bin/activate"
echo "  python run.py"
echo ""
echo "📚 Consulta README_INSTALL.md para más información"
echo ""

# Preguntar si ejecutar ahora
read -p "¿Deseas ejecutar la aplicación ahora? (s/n): " EJECUTAR

if [[ $EJECUTAR =~ ^[Ss]$ ]]; then
    echo -e "\n${YELLOW}Iniciando aplicación...${NC}\n"
    python run.py
else
    echo -e "\nPuedes ejecutar la aplicación más tarde con: ${BLUE}./ejecutar.sh${NC}\n"
fi