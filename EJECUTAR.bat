@echo off
chcp 65001 >nul

echo.
echo ============================================================
echo   📄 CV GENERATOR
echo ============================================================
echo.

REM Verificar si existe el entorno virtual
if not exist .env\Scripts\activate.bat (
    echo ❌ ERROR: El entorno virtual no existe
    echo.
    echo 💡 Ejecuta primero INSTALAR.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
call .env\Scripts\activate.bat

REM Ejecutar aplicación
python run.py

pause