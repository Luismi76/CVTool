# 🔄 Guía de Migración - CV Generator v2.0

Esta guía te ayudará a migrar de la versión anterior a la versión optimizada.

## 📋 Resumen de Cambios

### ✨ Nuevas Características

1. **Configuración Centralizada** (`config.py`)
   - Variables de entorno
   - Configuración por entorno (dev/prod)
   - Constantes centralizadas

2. **Manejo Robusto de Archivos** (`file_handler.py`)
   - Backups automáticos
   - Escritura atómica
   - Manejo de errores mejorado

3. **Validación Completa** (`validators.py`)
   - Validación de email, teléfono, URLs
   - Validación por tipo de sección
   - Mensajes de error descriptivos

4. **Logging Profesional**
   - Archivo `cv_generator.log`
   - Niveles de log apropiados
   - Información de contexto

5. **Scripts de Instalación**
   - Windows: `INSTALAR.bat`, `EJECUTAR.bat`
   - Linux/macOS: `instalar.sh`, `ejecutar.sh`
   - Instalación automática en un clic

6. **Páginas de Error Personalizadas**
   - 404.html
   - 500.html

## 🗂️ Estructura Nueva vs Antigua

### Antes (v1.0)
```
cv-generator/
├── app_dist.py          # Todo el código
├── cv_app.py            # Código duplicado
├── templates/
├── static/
├── render_templates/
└── data/
```

### Después (v2.0)
```
cv-generator/
├── app/
│   ├── config.py            # ⭐ Nuevo
│   ├── file_handler.py      # ⭐ Nuevo
│   ├── validators.py        # ⭐ Nuevo
│   └── app_refactored.py    # ⭐ Mejorado
├── templates/
│   ├── 404.html             # ⭐ Nuevo
│   └── 500.html             # ⭐ Nuevo
├── static/
├── render_templates/
├── data/
├── run.py                   # ⭐ Nuevo
├── INSTALAR.bat             # ⭐ Nuevo
├── EJECUTAR.bat             # ⭐ Nuevo
├── instalar.sh              # ⭐ Nuevo
├── ejecutar.sh              # ⭐ Nuevo
├── .env.example             # ⭐ Nuevo
├── README_INSTALL.md        # ⭐ Nuevo
└── BEST_PRACTICES.md        # ⭐ Nuevo
```

## 📦 Pasos de Migración

### Opción 1: Instalación Limpia (Recomendado)

Si no tienes datos importantes:

1. **Hacer backup de datos** (opcional)
   ```bash
   # Copiar carpeta data
   cp -r data data_backup
   ```

2. **Clonar versión nueva**
   ```bash
   git clone https://github.com/tuusuario/cv-generator.git cv-generator-v2
   cd cv-generator-v2
   ```

3. **Instalar**
   ```bash
   # Windows
   INSTALAR.bat
   
   # Linux/macOS
   chmod +x instalar.sh
   ./instalar.sh
   ```

4. **Restaurar datos** (si hiciste backup)
   ```bash
   cp -r ../cv-generator-v1/data ./data
   ```

### Opción 2: Actualización In-Place

Si quieres mantener la instalación actual:

1. **Backup completo**
   ```bash
   cp -r cv-generator cv-generator-backup
   ```

2. **Descargar archivos nuevos**
   - Crear carpeta `app/`
   - Descargar `config.py`, `file_handler.py`, `validators.py`
   - Descargar `run.py`
   - Descargar scripts de instalación

3. **Actualizar archivos existentes**
   - Reemplazar `requirements.txt`
   - Añadir `.env.example`
   - Añadir templates de error

4. **Mantener tus datos**
   - La carpeta `data/` se mantiene intacta
   - `cv.json` y `templates.json` siguen funcionando

5. **Reinstalar dependencias**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 🔧 Cambios en el Código

### Configuración

#### Antes
```python
DATA_DIR = os.environ.get("CVTOOL_DATA_DIR", os.path.join(APP_DIR, "data"))
```

#### Después
```python
from config import Config
DATA_DIR = Config.DATA_DIR
```

### Manejo de Archivos

#### Antes
```python
with open(path, "r") as f:
    return json.load(f)
```

#### Después
```python
from file_handler import CVDataHandler
data_handler = CVDataHandler(cv_file, templates_file)
cv = data_handler.load_cv()
```

### Validación

#### Antes
```python
# Sin validación o validación básica
cv["contact"] = request.form.get("contact")
```

#### Después
```python
from validators import ContactValidator
is_valid, errors = ContactValidator.validate_contact_data(contact_data)
if not is_valid:
    for error in errors:
        flash(error, 'error')
```

## 🗃️ Compatibilidad de Datos

### ✅ Archivos Compatibles

Los siguientes archivos **NO** necesitan cambios:

- ✅ `data/cv.json` - Estructura idéntica
- ✅ `data/templates.json` - Estructura idéntica
- ✅ `data/output/*` - CVs generados
- ✅ `templates/*.html` - Sin cambios mayores
- ✅ `static/*` - Sin cambios
- ✅ `render_templates/*.j2` - Sin cambios

### ⚠️ Archivos Deprecados

Estos archivos ya no se usan:

- ❌ `app_dist.py` - Reemplazado por `app/app_refactored.py`
- ❌ `cv_app.py` - Funcionalidad integrada en nuevo código

**Puedes eliminarlos** después de verificar que todo funciona.

## 🎯 Características que Debes Conocer

### 1. Variables de Entorno

Ahora puedes configurar la aplicación con archivo `.env`:

```bash
# Crear archivo .env
cp .env.example .env

# Editar según necesites
FLASK_ENV=development
PORT=5000
CVTOOL_DATA_DIR=/ruta/personalizada
```

### 2. Logging

La aplicación ahora registra todo en `cv_generator.log`:

```bash
# Ver logs en tiempo real
tail -f cv_generator.log

# Buscar errores
grep ERROR cv_generator.log
```

### 3. Validación Mejorada

Los formularios ahora validan:
- ✅ Formato de email
- ✅ Formato de teléfono
- ✅ URLs válidas
- ✅ Fechas en formato correcto
- ✅ Longitud de textos

### 4. Mensajes Flash

Sistema de notificaciones mejorado:
- ✅ Success (verde)
- ❌ Error (rojo)
- ⚠️ Warning (amarillo)
- ℹ️ Info (azul)

### 5. Backups Automáticos

Cada vez que guardas datos, se crea un backup automático en `data/backups/`.

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Config not found"

Asegúrate de tener la estructura correcta:
```bash
cv-generator/
├── app/
│   └── config.py  # Debe existir
```

### Datos no se guardan

Verifica permisos:
```bash
# Linux/macOS
chmod -R u+w data/

# Windows (como administrador)
icacls data /grant Users:F /T
```

### Aplicación no inicia

Revisa el log:
```bash
cat cv_generator.log
# o
type cv_generator.log  # Windows
```

## 📊 Verificación Post-Migración

### Checklist

- [ ] ✅ Aplicación inicia sin errores
- [ ] ✅ Puedo ver la página principal
- [ ] ✅ Mis datos del CV siguen ahí
- [ ] ✅ Puedo añadir nuevos items
- [ ] ✅ Puedo editar items existentes
- [ ] ✅ La personalización funciona
- [ ] ✅ Puedo generar CVs
- [ ] ✅ Mis plantillas guardadas funcionan

### Comandos de Verificación

```bash
# Verificar estructura
ls -la app/

# Verificar permisos
ls -la data/

# Verificar logs
tail cv_generator.log

# Probar aplicación
python run.py
```

## 🆘 Rollback (Volver Atrás)

Si algo no funciona, puedes volver a la versión anterior:

```bash
# Si hiciste backup
rm -rf cv-generator
mv cv-generator-backup cv-generator
cd cv-generator

# Activar entorno y ejecutar
source cv_env/bin/activate  # o cv_env\Scripts\activate en Windows
python app_dist.py
```

## 📞 Soporte

Si tienes problemas durante la migración:

1. Revisa `cv_generator.log`
2. Consulta [README_INSTALL.md](README_INSTALL.md)
3. Busca en [GitHub Issues](https://github.com/tuusuario/cv-generator/issues)
4. Crea un nuevo Issue con:
   - Versión anterior que usabas
   - Pasos que seguiste
   - Error completo
   - Contenido del log

## 🎉 Beneficios de la Migración

Después de migrar tendrás:

- ✅ Código más organizado y mantenible
- ✅ Instalación en un clic
- ✅ Validación robusta de datos
- ✅ Backups automáticos
- ✅ Logging profesional
- ✅ Mejor manejo de errores
- ✅ Documentación completa
- ✅ Seguimiento de mejores prácticas

---

**¿Preguntas?** Abre un Issue en GitHub o consulta la documentación.

**Última actualización:** Octubre 2025  
**Versión objetivo:** 2.0  
**Compatibilidad:** Datos de v1.0 totalmente compatibles