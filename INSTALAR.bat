@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo   📄 CV GENERATOR - Instalación Automática
echo ============================================================
echo.
echo Este script instalará CV Generator automáticamente.
echo.
pause

echo.
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo 💡 Por favor, instala Python desde: https://www.python.org/downloads/
    echo    Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [2/5] Creando entorno virtual...
if exist cv_env (
    echo ⚠️  El entorno virtual ya existe. Eliminando...
    rmdir /s /q cv_env
)
python -m venv cv_env
if errorlevel 1 (
    echo ❌ ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual creado

echo.
echo [3/5] Activando entorno virtual...
call cv_env\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado

echo.
echo [4/5] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [5/5] Creando archivo de configuración...
if not exist .env (
    copy .env.example .env >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  No se pudo crear .env automáticamente
        echo    Puedes copiarlo manualmente más tarde
    ) else (
        echo ✅ Archivo .env creado
    )
) else (
    echo ℹ️  Archivo .env ya existe
)

echo.
echo ============================================================
echo   🎉 ¡Instalación completada con éxito!
echo ============================================================
echo.
echo Para ejecutar la aplicación:
echo   1. Doble clic en EJECUTAR.bat
echo   O desde la consola:
echo      cv_env\Scripts\activate
echo      python run.py
echo.
echo 📚 Consulta README_INSTALL.md para más información
echo.
pause

echo.
echo ¿Deseas ejecutar la aplicación ahora? (S/N)
set /p EJECUTAR=Respuesta: 

if /i "%EJECUTAR%"=="S" (
    echo.
    echo Iniciando aplicación...
    python run.py
) else (
    echo.
    echo Puedes ejecutar la aplicación más tarde con EJECUTAR.bat
    echo.
    pause
)