from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from app.routes import personalization_bp
import logging

logger = logging.getLogger(__name__)

@personalization_bp.route('/personalizar')
def customize():
    """Página de personalización del CV"""
    try:
        cv = current_app.data_handler.load_cv()
        templates = current_app.data_handler.load_templates()
        return render_template(
            "customize.html", 
            cv=cv, 
            templates=templates, 
            title="Personalizar CV"
        )
    except Exception as e:
        logger.error(f"Error en customize: {e}")
        flash('Error al cargar datos de personalización', 'error')
        return redirect(url_for('main.index'))

@personalization_bp.route('/personalizar/plantilla/<template_name>')
def load_template(template_name):
    """Carga una plantilla guardada"""
    try:
        templates = current_app.data_handler.load_templates()
        
        if template_name in templates:
            return jsonify(templates[template_name])
        
        return jsonify({"error": "Plantilla no encontrada"}), 404
        
    except Exception as e:
        logger.error(f"Error al cargar plantilla {template_name}: {e}")
        return jsonify({"error": "Error al cargar plantilla"}), 500

@personalization_bp.route('/personalizar/guardar', methods=['POST'])
def save_template():
    """Guarda una plantilla de selección"""
    try:
        data = request.get_json()
        template_name = data.get("name", "").strip()
        
        if not template_name:
            return jsonify({"error": "Nombre de plantilla requerido"}), 400
        
        # Validar nombre
        if len(template_name) > 50:
            return jsonify({"error": "Nombre demasiado largo (máx. 50 caracteres)"}), 400
        
        templates = current_app.data_handler.load_templates()
        
        templates[template_name] = {
            "name": template_name,
            "description": data.get("description", ""),
            "selection": data.get("selection", {}),
            "created": data.get("created", "")
        }
        
        if current_app.data_handler.save_templates(templates):
            logger.info(f"Plantilla '{template_name}' guardada")
            return jsonify({
                "success": True, 
                "message": "Plantilla guardada correctamente"
            })
        else:
            return jsonify({"error": "Error al guardar plantilla"}), 500
            
    except Exception as e:
        logger.error(f"Error al guardar plantilla: {e}")
        return jsonify({"error": "Error inesperado"}), 500

@personalization_bp.route('/personalizar/eliminar/<template_name>', methods=['POST'])
def delete_template(template_name):
    """Elimina una plantilla guardada"""
    try:
        templates = current_app.data_handler.load_templates()
        
        if template_name in templates:
            del templates[template_name]
            
            if current_app.data_handler.save_templates(templates):
                logger.info(f"Plantilla '{template_name}' eliminada")
                return jsonify({
                    "success": True, 
                    "message": "Plantilla eliminada"
                })
            else:
                return jsonify({"error": "Error al eliminar plantilla"}), 500
        
        return jsonify({"error": "Plantilla no encontrada"}), 404
        
    except Exception as e:
        logger.error(f"Error al eliminar plantilla {template_name}: {e}")
        return jsonify({"error": "Error inesperado"}), 500
