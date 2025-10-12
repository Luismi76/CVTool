# CVTool

<p align="left">
  <a href="https://github.com/Luismi76/CVTool"><img alt="Repo" src="https://img.shields.io/badge/GitHub-CVTool-181717?logo=github"></a>
  <a href="https://github.com/Luismi76/CVTool/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue.svg">
  <img alt="Framework" src="https://img.shields.io/badge/Framework-Flask-orange.svg">
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/Luismi76/CVTool.svg">
  <img alt="Issues" src="https://img.shields.io/github/issues/Luismi76/CVTool.svg">
  <img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Luismi76/CVTool.svg">
  <img alt="Stars" src="https://img.shields.io/github/stars/Luismi76/CVTool.svg?style=social">
</p>

**CVTool** es una aplicación web escrita en Python que permite generar y gestionar currículums de forma flexible desde una interfaz local sencilla.  
El proyecto está diseñado para que el usuario final pueda descargar un único archivo ejecutable (`.exe`) y utilizarlo sin necesidad de instalar dependencias manualmente.

---

## 📁 Estructura del proyecto

```
CVTool/
├── app/                   # Código fuente principal de la aplicación (lógica Flask)
├── backup_old_files/      # Archivos antiguos o en desuso
├── data/                  # Datos auxiliares o de prueba
├── dist/                  # Artefactos generados (.exe)
├── render_templates/      # Plantillas adicionales para renderizado
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── templates/             # Plantillas HTML de la interfaz
├── .env.example           # Ejemplo de configuración de entorno
├── BEST_PRACTICES.md      # Buenas prácticas
├── MIGRATION_GUIDE.md     # Guía de migraciones
├── README_INSTALL.md      # Instrucciones de instalación detalladas
├── run.py                 # Punto de entrada principal
├── requirements.txt       # Dependencias Python
└── instalar.sh / ejecutar.sh / *.bat  # Scripts auxiliares
```

---

## ⚙️ Requisitos para desarrollo

Si quieres ejecutar el proyecto desde código fuente:

- Python 3.11 (recomendado)
- pip
- virtualenv (opcional)

---

## 🧰 Instalación (modo desarrollo)

```powershell
git clone https://github.com/Luismi76/CVTool.git
cd CVTool
py -3.11 -m venv .venv311
.\.venv311\Scripts\Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python run.py
```

Luego abre en el navegador:

```
http://127.0.0.1:5000
```

---

## 🏗️ Generar el ejecutable (.exe)

1. Asegúrate de tener activado el entorno con Python 3.11.

2. Ejecuta el empaquetado con PyInstaller:
   
   ```powershell
   pyinstaller --onefile --noconsole --name CV_Generator `
   --add-data "templates;templates" `
   --add-data "static;static" `
   --add-data "render_templates;render_templates" `
   run.py
   ```

3. El archivo final estará en:
   
   ```
   dist\CV_Generator.exe
   ```

4. Ejecuta el `.exe` para iniciar la aplicación. Se abrirá automáticamente en tu navegador:
   
   ```
   http://127.0.0.1:5000
   ```

---

## 🚀 Publicar el .exe en GitHub Releases (manual)

1. **Genera el .exe** como se indica arriba.
2. Crea un tag en Git:
   
   ```powershell
   git tag v0.1.0
   git push origin v0.1.0
   ```
3. Ve a [Releases](https://github.com/Luismi76/CVTool/releases) → **Draft a new release**.
4. Selecciona el tag `v0.1.0`, pon título y descripción.
5. **Arrastra `dist/CV_Generator.exe` al apartado “Assets”**.
6. Pulsa **Publish release**.

El ejecutable aparecerá como archivo descargable.

---

## 📝 Scripts útiles

- `instalar.sh` / `instalar.bat`: instalación automatizada.
- `ejecutar.sh` / `ejecutar.bat`: ejecución rápida local.

---

## 🧭 Roadmap

- 📝 Integrar funciones avanzadas de gestión de CV.
- 🧰 Mejorar la interfaz web.
- 🌐 Añadir soporte para múltiples plantillas.
- 🚀 Publicación automatizada de binarios.

---

## 🤝 Contribuir

1. Haz un **fork** del repositorio.
2. Crea una rama:
   
   ```bash
   git checkout -b feature/mi-mejora
   ```
3. Realiza tus cambios y tests.
4. Envía un Pull Request.

---

## 📄 Licencia MIT

Este proyecto está licenciado bajo los términos de la **Licencia MIT**.

```
MIT License

Copyright (c) 2025 Luismi76

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📌 Créditos

Desarrollado por [Luismi76](https://github.com/Luismi76).  
Proyecto en evolución orientado a simplificar la creación de CVs locales sin instalación de dependencias complejas.
