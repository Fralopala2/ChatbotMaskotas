#!/bin/bash
# Script de configuración rápida para Chatbot Maskotas (macOS/Linux)
# Este script configura todo lo necesario para ejecutar el chatbot

echo "===================================================="
echo "  Chatbot Maskotas - Configuración Inicial"
echo "===================================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no está instalado"
    echo "Descargalo desde: https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python3 encontrado"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo ""
    echo "[*] Creando entorno virtual..."
    python3 -m venv venv
    echo "[OK] Entorno virtual creado"
else
    echo "[OK] Entorno virtual ya existe"
fi

# Activar entorno virtual
echo ""
echo "[*] Activando entorno virtual..."
source venv/bin/activate
echo "[OK] Entorno virtual activado"

# Instalar dependencias
echo ""
echo "[*] Instalando dependencias..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "[OK] Dependencias instaladas"
else
    echo "[ERROR] Error al instalar dependencias"
    exit 1
fi

# Crear directorio de logs
if [ ! -d "logs" ]; then
    mkdir logs
    echo "[OK] Directorio de logs creado"
fi

# Verificar configuración
echo ""
echo "[*] Verificando configuración..."
python3 -c "from config import validate_config; validate_config(); print('[OK] Configuración válida')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] La configuración no es válida"
    echo ""
    echo "[!] Por favor, realiza lo siguiente:"
    echo "   1. Copia .env.example a .env"
    echo "   2. Edita .env y agrega tu GOOGLE_API_KEY"
    echo "   3. Asegúrate de que el archivo Firebase JSON existe"
    echo ""
    exit 1
fi

# Preguntar si subir datos
echo ""
read -p "[?] ¿Deseas subir la base de conocimientos a Firestore? (s/n): " upload
if [ "$upload" = "s" ] || [ "$upload" = "S" ]; then
    echo ""
    echo "[*] Subiendo base de conocimientos..."
    python3 upload_data_improved.py
    if [ $? -eq 0 ]; then
        echo "[OK] Base de conocimientos subida exitosamente"
    else
        echo "[!] Error al subir la base de conocimientos"
        echo "     Puedes intentar más tarde ejecutando: python3 upload_data_improved.py"
    fi
fi

# Iniciar chatbot
echo ""
echo "===================================================="
echo "  ¡Iniciando Chatbot Maskotas!"
echo "===================================================="
echo ""

python3 chatbot.py

# Fin
echo ""
echo "===================================================="
echo "  ¡Gracias por usar Chatbot Maskotas!"
echo "===================================================="
