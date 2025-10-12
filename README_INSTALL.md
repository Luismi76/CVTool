# 📦 Guía de Instalación - CV Generator

Esta guía te ayudará a instalar y ejecutar CV Generator paso a paso, incluso sin conocimientos técnicos previos.

## 🎯 Requisitos Previos

### Windows
- Python 3.8 o superior ([Descargar aquí](https://www.python.org/downloads/))
  - ⚠️ Durante la instalación, marca la casilla "Add Python to PATH"

### macOS
- Python 3.8 o superior (viene preinstalado, o instalar con Homebrew)
```bash
brew install python3
```

### Linux
- Python 3.8 o superior
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 Instalación Rápida (Recomendada)

### Opción 1: Script Automático

#### Windows
1. Descarga el proyecto
2. Doble clic en `INSTALAR.bat`
3. Sigue las instrucciones en pantalla

#### Linux/macOS
1. Abre la terminal en la carpeta del proyecto
2. Ejecuta:
```bash
chmod +x instalar.sh
./instalar.sh
```

### Opción 2: Instalación Manual

#### Paso 1: Descargar el Proyecto
```bash
# Si tienes Git instalado
git clone https://github.com/tuusuario/cv-generator.git
cd cv-generator

# O descarga el ZIP desde GitHub y extráelo
```

#### Paso 2: Crear Entorno Virtual

**Windows:**
```cmd
python -m venv cv_env
cv_env\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv cv_env
source cv_env/bin/activate
```

#### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar Variables de Entorno (Opcional)
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus preferencias
# (puedes usar cualquier editor de texto)
```

#### Paso 5: Ejecutar la Aplicación
```bash
python run.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://127.0.0.1:5000`

## 🎨 Estructura del Proyecto

```
cv-generator/
├── app/                      # Código de la aplicación
│   ├── config.py            # Configuración
│   ├── file_handler.py      # Manejo de archivos
│   ├── validators.py        # Validaciones
│   └── app_refactored.py    # Aplicación principal
├── static/                   # Archivos estáticos (CSS, JS)
├── templates/                # Plantillas HTML
├── render_templates/         # Plantillas de CV (Markdown, TXT)
├── data/                     # Datos del usuario (se crea automáticamente)
│   ├── cv.json              # Tu información
│   ├── templates.json       # Plantillas guardadas
│   └── output/              # CVs generados
├── requirements.txt          # Dependencias
├── run.py                   # Script de ejecución
├── .env.example             # Ejemplo de configuración
└── README.md                # Documentación principal
```

## ⚙️ Configuración Avanzada

### Variables de Entorno Disponibles

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `FLASK_ENV` | Entorno de ejecución | `development` |
| `SECRET_KEY` | Clave secreta de Flask | `dev-secret-key...` |
| `HOST` | Dirección del servidor | `127.0.0.1` |
| `PORT` | Puerto del servidor | `5000` |
| `CVTOOL_DATA_DIR` | Carpeta de datos | `./data` |
| `DEBUG` | Modo debug | `True` |

### Cambiar Puerto de Ejecución

Si el puerto 5000 está ocupado:

**Método 1: Variable de entorno**
```bash
# Windows
set PORT=8080
python run.py

# Linux/macOS
PORT=8080 python run.py
```

**Método 2: Archivo .env**
```bash
# En .env
PORT=8080
```

### Usar Directorio de Datos Personalizado

```bash
# En .env
CVTOOL_DATA_DIR=/ruta/a/tu/carpeta/datos
```

## 🔧 Solución de Problemas

### Error: "Python no se reconoce como comando"

**Windows:**
1. Reinstala Python marcando "Add Python to PATH"
2. O añade Python al PATH manualmente

**Linux/macOS:**
```bash
# Usa python3 en lugar de python
python3 run.py
```

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de estar en el entorno virtual
# Windows
cv_env\Scripts\activate

# Linux/macOS
source cv_env/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Port already in use"

El puerto 5000 está ocupado. Usa otro puerto:
```bash
PORT=8080 python run.py
```

### Error: "Permission Denied"

**Linux/macOS:**
```bash
# Da permisos de ejecución
chmod +x run.py
chmod +x instalar.sh
```

### La aplicación no se abre en el navegador

Abre manualmente tu navegador y visita:
```
http://127.0.0.1:5000
```

### Error al guardar datos

Verifica que tienes permisos de escritura en la carpeta del proyecto:
```bash
# Linux/macOS
chmod -R u+w ./data
```

## 🐳 Instalación con Docker (Opcional)

Si prefieres usar Docker:

```bash
# Construir imagen
docker build -t cv-generator .

# Ejecutar contenedor
docker run -p 5000:5000 -v $(pwd)/data:/app/data cv-generator
```

## 🔄 Actualización

Para actualizar a la última versión:

```bash
# Con Git
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Reiniciar aplicación
python run.py
```

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa el log:** `cv_generator.log` en la carpeta del proyecto
2. **Busca en Issues:** [GitHub Issues](https://github.com/tuusuario/cv-generator/issues)
3. **Crea un Issue:** Describe tu problema con:
   - Sistema operativo
   - Versión de Python
   - Mensaje de error completo
   - Pasos para reproducir el problema

## 📚 Recursos Adicionales

- [Documentación completa](README.md)
- [Manual de usuario](docs/user-guide.md)
- [Preguntas frecuentes](docs/FAQ.md)
- [Ejemplos de plantillas](docs/template-examples.md)

## ✅ Verificación de Instalación

Después de instalar, verifica que todo funciona:

```bash
# Activar entorno virtual
# Windows: cv_env\Scripts\activate
# Linux/macOS: source cv_env/bin/activate

# Ejecutar aplicación
python run.py

# Deberías ver:
# ============================================================
# CV GENERATOR - Generador de Currículums Profesional
# ============================================================
# 🚀 Iniciando aplicación...
#    Entorno: development
#    URL: http://127.0.0.1:5000
# ...
```

Si ves este mensaje, ¡la instalación fue exitosa! 🎉

## 🎓 Próximos Pasos

1. Abre la aplicación en tu navegador
2. Completa tu información de contacto
3. Añade tu experiencia y habilidades
4. Prueba la función de personalización
5. Genera tu primer CV

---

**¿Necesitas ayuda?** No dudes en abrir un Issue en GitHub o consultar la documentación completa.