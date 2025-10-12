#!/bin/bash

# Script de ejecución para CV Generator (Linux/macOS)

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}============================================================${NC}"
echo -e "${BLUE}  📄 CV GENERATOR${NC}"
echo -e "${BLUE}============================================================${NC}\n"

# Verificar si existe el entorno virtual
if [ ! -d "cv_env" ]; then
    echo -e "${RED}❌ ERROR: El entorno virtual no existe${NC}\n"
    echo -e "💡 Por favor, ejecuta primero: ${BLUE}./instalar.sh${NC}\n"
    exit 1
fi

# Activar entorno virtual
source cv_env/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ ERROR: No se pudo activar el entorno virtual${NC}\n"
    echo -e "💡 Intenta ejecutar ${BLUE}./instalar.sh${NC} nuevamente\n"
    exit 1
fi

echo -e "${GREEN}✅ Entorno virtual activado${NC}\n"

# Ejecutar aplicación
python run.py

# Capturar código de salida
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo -e "\n${RED}❌ La aplicación se cerró con un error${NC}"
    echo -e "💡 Revisa el archivo ${BLUE}cv_generator.log${NC} para más detalles\n"
fi

exit $EXIT_CODE