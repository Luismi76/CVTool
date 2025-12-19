import os
import sys
import logging
from flask import Flask
from jinja2 import Environment, FileSystemLoader
from app.file_handler import CVDataHandler
from app.validators import ContactValidator
from flask_session import Session

__version__ = '0.2.0'

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cv_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """
    Factory para crear la aplicación
    """
    from app.config import get_config
    
    config_class = get_config(config_name)
    app = Flask(__name__)
    
    # Aplicar configuración
    app.config.from_object(config_class)
    app.secret_key = config_class.SECRET_KEY
    
    # Adjuntar objeto de configuración para acceso directo a atributos de clase
    app.config_obj = config_class
    
    # Inicializar directorios
    config_class.init_app()
    
    # Configurar sesiones
    if config_class.USE_SESSION_STORAGE:
        session_dir = config_class.DATA_DIR / 'flask_session'
        session_dir.mkdir(parents=True, exist_ok=True)
        
        app.config['SESSION_TYPE'] = 'filesystem'
        app.config['SESSION_PERMANENT'] = False
        app.config['SESSION_USE_SIGNER'] = True
        app.config['SESSION_FILE_DIR'] = str(session_dir)
        Session(app)
    
    # Configurar templates y static de forma explicita si es necesario
    app.template_folder = str(config_class.BASE_DIR / "templates")
    app.static_folder = str(config_class.BASE_DIR / "static")

    # Configurar Jinja2 personalizado
    # Nota: Flask ya tiene su propio jinja_env, pero si queremos usar el loader especifico:
    my_loader = FileSystemLoader(str(config_class.TEMPLATES_DIR))
    # Sin embargo, Flask usa app.jinja_loader.
    # Para mantener compatibilidad con codigo existente que usa app.jinja_env en generator.py:
    # Vamos a configurar el entorno principal de Flask para que busque tambien en TEMPLATES_DIR
    # O mejor, adjuntamos un jinja_env secundario si es necesario para los templates de texto/md
    
    # Configurar loader modificado para buscar en templates y render_templates
    # app.jinja_loader = FileSystemLoader([str(config_class.BASE_DIR / "templates"), str(config_class.TEMPLATES_DIR)])
    
    # Pero el código de app_refactored usaba un Environment separado para _render_to_text.
    # Lo recreamos y adjuntamos a app
    app.jinja_env_custom = Environment(
        loader=FileSystemLoader(str(config_class.TEMPLATES_DIR)),
        autoescape=False,
        trim_blocks=False,
        lstrip_blocks=False
    )
    # Monkey patch para que generator.py funcione con current_app.jinja_env (refeririendose al custom)
    # O mejor, actualizamos generator.py para usar app.jinja_env_custom si fuera necesario, 
    # pero generator.py usaba `current_app.jinja_env`. 
    # En Flask `current_app.jinja_env` es el entorno por defecto.
    # Vamos a añadir TEMPLATES_DIR al loader por defecto de Flask
    from jinja2 import ChoiceLoader
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(str(config_class.TEMPLATES_DIR)), # Prioridad a los templates de render
        app.jinja_loader
    ])
    
    # Inicializar manejadores
    app.data_handler = CVDataHandler(
        config_class.CV_TEMPLATE_FILE,
        config_class.TEMPLATES_FILE,
        use_session=config_class.USE_SESSION_STORAGE
    )
    app.contact_validator = ContactValidator()
    
    # Registrar Blueprints
    from app.routes import main_bp, sections_bp, personalization_bp, generator_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(sections_bp)
    app.register_blueprint(personalization_bp)
    app.register_blueprint(generator_bp)
    
    # Manejadores de errores
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_error)
    
    logger.info(f"Aplicación inicializada: {config_name}")
    return app

def not_found(error):
    from flask import render_template
    return render_template('404.html'), 404

def internal_error(error):
    from flask import render_template
    return render_template('500.html'), 500
