from flask import Blueprint

# Definir Blueprints
main_bp = Blueprint('main', __name__)
sections_bp = Blueprint('sections', __name__)
personalization_bp = Blueprint('personalization', __name__)
generator_bp = Blueprint('generator', __name__)

# Importar rutas para registrarlas
from app.routes import main, sections, personalization, generator
