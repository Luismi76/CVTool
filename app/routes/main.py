from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from app.routes import main_bp
from app.validators import Validator
import logging
import json
from datetime import datetime
from io import BytesIO

logger = logging.getLogger(__name__)

# ===== RUTAS PRINCIPALES =====

@main_bp.route('/')
def index():
    """Página principal"""
    try:
        cv = current_app.data_handler.load_cv()
        logger.debug(f"CV cargado: {len(cv.get('experience', []))} experiencias")
        return render_template("index.html", cv=cv, title="Inicio")
    except Exception as e:
        logger.error(f"Error en index: {e}")
        flash("Error al cargar los datos", "error")
        return render_template("index.html", cv=current_app.config_obj.get_empty_cv(), title="Inicio")

@main_bp.route('/acerca')
def about():
    """Página acerca de"""
    return render_template("about.html", title="Acerca de")

# ===== CONTACTO Y RESUMEN =====

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Gestión de datos de contacto"""
    cv = current_app.data_handler.load_cv()
    
    if request.method == 'POST':
        try:
            # Recopilar datos del formulario
            contact_data = {
                'name': request.form.get('name', '').strip(),
                'title': request.form.get('title', '').strip(),
                'location': request.form.get('location', '').strip(),
                'email': request.form.get('email', '').strip(),
                'phone': request.form.get('phone', '').strip(),
            }
            
            # Procesar links
            links_str = request.form.get('links', '').strip()
            contact_data['links'] = [
                link.strip() for link in links_str.split(',') 
                if link.strip()
            ]
            
            # Validar datos
            is_valid, errors = current_app.contact_validator.validate_contact_data(contact_data)
            
            if not is_valid:
                for error in errors:
                    flash(error, 'error')
                return render_template("contact.html", cv=cv, title="Contacto")
            
            # Guardar datos
            cv['contact'] = contact_data
            if current_app.data_handler.save_cv(cv):
                flash('Contacto guardado correctamente', 'success')
                logger.info("Datos de contacto actualizados")
                return redirect(url_for('main.contact'))
            else:
                flash('Error al guardar los datos', 'error')
                
        except Exception as e:
            logger.error(f"Error al guardar contacto: {e}")
            flash('Error inesperado al guardar', 'error')
    
    return render_template("contact.html", cv=cv, title="Contacto")

@main_bp.route('/summary', methods=['GET', 'POST'])
def summary():
    """Gestión del resumen profesional"""
    cv = current_app.data_handler.load_cv()
    
    if request.method == 'POST':
        try:
            summary_text = request.form.get('summary', '').strip()
            
            # Validar longitud
            is_valid, error = Validator.validate_text_length(
                summary_text, 
                min_len=0, 
                max_len=2000
            )
            
            if not is_valid:
                flash(error, 'error')
                return render_template("summary.html", cv=cv, title="Resumen")
            
            cv['summary'] = summary_text
            if current_app.data_handler.save_cv(cv):
                flash('Resumen guardado correctamente', 'success')
                logger.info("Resumen actualizado")
                return redirect(url_for('main.summary'))
            else:
                flash('Error al guardar el resumen', 'error')
                
        except Exception as e:
            logger.error(f"Error al guardar resumen: {e}")
            flash('Error inesperado al guardar', 'error')
    
    return render_template("summary.html", cv=cv, title="Resumen")

# ===== GESTIÓN DE DATOS DEL USUARIO =====

@main_bp.route('/limpiar-cv', methods=['POST'])
def clear_cv():
    """Limpia todos los datos del CV del usuario actual"""
    try:
        if current_app.data_handler.clear_cv():
            flash('Todos los datos han sido eliminados', 'success')
            logger.info("CV limpiado por el usuario")
        else:
            flash('Error al limpiar los datos', 'error')
    except Exception as e:
        logger.error(f"Error al limpiar CV: {e}")
        flash('Error inesperado', 'error')
    
    return redirect(url_for('main.index'))

@main_bp.route('/importar-cv', methods=['POST'])
def import_cv():
    """Importa datos de CV desde un archivo JSON"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No se encontró archivo"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Archivo vacío"}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({"error": "Solo se permiten archivos .json"}), 400
        
        # Leer y validar JSON
        content = file.read().decode('utf-8')
        cv_data = json.loads(content)
        
        # Validar estructura básica
        if not isinstance(cv_data, dict):
            return jsonify({"error": "Formato de archivo inválido"}), 400
        
        # Guardar en sesión del usuario
        if current_app.data_handler.save_cv(cv_data):
            logger.info("CV importado correctamente")
            return jsonify({
                "success": True,
                "message": "CV importado correctamente"
            })
        else:
            return jsonify({"error": "Error al guardar los datos"}), 500
        
    except json.JSONDecodeError:
        return jsonify({"error": "Archivo JSON inválido"}), 400
    except Exception as e:
        logger.error(f"Error al importar CV: {e}")
        return jsonify({"error": "Error inesperado al importar"}), 500

@main_bp.route('/exportar-cv', methods=['GET'])
def export_cv():
    """Exporta los datos del CV actual como archivo JSON"""
    from flask import send_file
    
    try:
        cv = current_app.data_handler.load_cv()
        
        # Crear archivo en memoria
        json_data = json.dumps(cv, indent=2, ensure_ascii=False)
        buffer = BytesIO(json_data.encode('utf-8'))
        buffer.seek(0)
        
        # Nombre del archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mi_cv_{timestamp}.json"
        
        logger.info("CV exportado")
        
        return send_file(
            buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error al exportar CV: {e}")
        flash('Error al exportar el CV', 'error')
        return redirect(url_for('main.index'))
