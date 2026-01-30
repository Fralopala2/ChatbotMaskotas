@echo off
REM Script de configuración rápida para Chatbot Maskotas (Windows)
REM Este script configura todo lo necesario para ejecutar el chatbot

echo ====================================================
echo  Chatbot Maskotas - Configuración Inicial
echo ====================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en PATH
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado

REM Crear entorno virtual
if not exist venv (
    echo.
    echo [*] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado
) else (
    echo [OK] Entorno virtual ya existe
)

REM Activar entorno virtual
echo.
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado

REM Instalar dependencias
echo.
echo [*] Instalando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% equ 0 (
    echo [OK] Dependencias instaladas
) else (
    echo [ERROR] Error al instalar dependencias
    pause
    exit /b 1
)

REM Crear directorio de logs
if not exist logs (
    mkdir logs
    echo [OK] Directorio de logs creado
)

REM Verificar configuración
echo.
echo [*] Verificando configuración...
python -c "from config import validate_config; validate_config(); print('[OK] Configuración válida')" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] La configuración no es válida
    echo.
    echo [!] Por favor, realiza lo siguiente:
    echo   1. Copia .env.example a .env
    echo   2. Edita .env y agrega tu GOOGLE_API_KEY
    echo   3. Asegúrate de que el archivo Firebase JSON existe
    echo.
    pause
    exit /b 1
)

REM Preguntar si subir datos
echo.
echo [?] ¿Deseas subir la base de conocimientos a Firestore?
set /p upload="Responde (s/n): "
if /i "%upload%"=="s" (
    echo.
    echo [*] Subiendo base de conocimientos...
    python upload_data_improved.py
    if %errorlevel% equ 0 (
        echo [OK] Base de conocimientos subida exitosamente
    ) else (
        echo [!] Error al subir la base de conocimientos
        echo     Puedes intentar más tarde ejecutando: python upload_data_improved.py
    )
)

REM Iniciar chatbot
echo.
echo ====================================================
echo  ¡Iniciando Chatbot Maskotas!
echo ====================================================
echo.

python chatbot.py

REM Fin
echo.
echo ====================================================
echo  ¡Gracias por usar Chatbot Maskotas!
echo ====================================================
pause
