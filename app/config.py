"""
Configuración centralizada de la aplicación CV Generator
ARCHIVO: app/config.py
"""
import os
from pathlib import Path

class Config:
    """Configuración base de la aplicación"""
    
    # Directorios base
    BASE_DIR = Path(__file__).parent.parent
    APP_DIR = BASE_DIR / "app"
    
    # Directorios de datos
    DATA_DIR = Path(os.environ.get("CVTOOL_DATA_DIR", BASE_DIR / "data"))
    OUT_DIR = DATA_DIR / "output"
    TEMPLATES_DIR = BASE_DIR / "render_templates"
    
    # Archivos de datos
    CV_FILE = DATA_DIR / "cv.json"
    TEMPLATES_FILE = DATA_DIR / "templates.json"
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    
    # Configuración de servidor
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", 5000))
    
    # Límites de datos
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_ITEMS_PER_SECTION = 100
    
    # Secciones del CV
    CV_SECTIONS = [
        "skills", "experience", "projects", 
        "education", "courses", "otros"
    ]
    
    # Campos por sección
    SECTION_FIELDS = {
        "skills": ["name", "level", "tags"],
        "experience": ["title", "company", "location", "start", "end", "description", "tech"],
        "projects": ["title", "company", "location", "start", "end", "description", "tech"],
        "education": ["degree", "institution", "start", "end", "notes"],
        "courses": ["name", "issuer", "date", "hours", "credential", "tags"],
        "otros": ["title", "institution", "start", "end", "periodo", "description", "tags"]
    }
    
    @classmethod
    def init_app(cls):
        """Inicializa directorios necesarios"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUT_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False


# Diccionario de configuraciones
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}


def get_config(env=None):
    """Obtiene la configuración según el entorno"""
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")
    return config.get(env, config["default"])