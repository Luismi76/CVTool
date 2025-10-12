"""
CV Generator - Aplicación Principal Refactorizada
Versión optimizada siguiendo mejores prácticas
"""
import os
import sys
import logging
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from jinja2 import Environment, FileSystemLoader
from app.file_handler import CVDataHandler
from app.validators import ContactValidator, ItemValidator, Validator

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


class CVGeneratorApp:
    """Clase principal de la aplicación"""
    
    def __init__(self, config_class):
        """
        Inicializa la aplicación
        
        Args:
            config_class: Clase de configuración a usar
        """
        self.app = Flask(__name__)
        self.config = config_class
        self.setup_app()
        self.setup_handlers()
        self.register_routes()
        
    def setup_app(self):
        """Configura la aplicación Flask"""
        # Aplicar configuración
        self.app.config.from_object(self.config)
        self.app.secret_key = self.config.SECRET_KEY 
        
        # Inicializar directorios
        self.config.init_app()
        
        # Configurar templates y static
        self.app.template_folder = str(self.config.BASE_DIR / "templates")
        self.app.static_folder = str(self.config.BASE_DIR / "static")
        
        # Configurar Jinja2 para renderizado
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.config.TEMPLATES_DIR)),
            autoescape=False,
            trim_blocks=False,
            lstrip_blocks=False
        )
        
        logger.info(f"Aplicación configurada: {self.config.__name__}")
    
    def setup_handlers(self):
        """Configura manejadores de datos"""
        self.data_handler = CVDataHandler(
            self.config.CV_FILE,
            self.config.TEMPLATES_FILE
        )
        self.contact_validator = ContactValidator()
    
    def register_routes(self):
        """Registra todas las rutas de la aplicación"""
        # Rutas principales
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/acerca', 'about', self.about)
        
        # Rutas de contacto y resumen
        self.app.add_url_rule('/contact', 'contact', self.contact, methods=['GET', 'POST'])
        self.app.add_url_rule('/summary', 'summary', self.summary, methods=['GET', 'POST'])
        
        # Rutas de secciones
        self.app.add_url_rule('/<section>', 'list_items', self.list_items)
        self.app.add_url_rule('/<section>/add', 'add_item', self.add_item, methods=['GET', 'POST'])
        self.app.add_url_rule('/<section>/edit/<int:idx>', 'edit_item', self.edit_item, methods=['GET', 'POST'])
        self.app.add_url_rule('/<section>/delete/<int:idx>', 'delete_item', self.delete_item)
        
        # Rutas de personalización
        self.app.add_url_rule('/personalizar', 'customize', self.customize)
        self.app.add_url_rule('/personalizar/plantilla/<template_name>', 'load_template', self.load_template)
        self.app.add_url_rule('/personalizar/guardar', 'save_template', self.save_template, methods=['POST'])
        self.app.add_url_rule('/personalizar/eliminar/<template_name>', 'delete_template', self.delete_template, methods=['POST'])
        
        # Rutas de preview y generación
        self.app.add_url_rule('/preview', 'preview', self.preview)
        self.app.add_url_rule('/preview/personalizada', 'preview_custom', self.preview_custom, methods=['POST'])
        self.app.add_url_rule('/generar', 'generate', self.generate, methods=['GET', 'POST'])
        self.app.add_url_rule('/generar/personalizado', 'generate_custom', self.generate_custom, methods=['POST'])
        self.app.add_url_rule('/download/<path:path>', 'download', self.download)
        
        # Manejadores de errores
        self.app.errorhandler(404)(self.not_found)
        self.app.errorhandler(500)(self.internal_error)
    
    # ===== RUTAS PRINCIPALES =====
    
    def index(self):
        """Página principal"""
        try:
            cv = self.data_handler.load_cv()
            return render_template("index.html", cv=cv, title="Inicio")
        except Exception as e:
            logger.error(f"Error en index: {e}")
            flash("Error al cargar los datos", "error")
            return render_template("index.html", cv={}, title="Inicio")
    
    def about(self):
        """Página acerca de"""
        return render_template("about.html", title="Acerca de")
    
    # ===== CONTACTO Y RESUMEN =====
    
    def contact(self):
        """Gestión de datos de contacto"""
        cv = self.data_handler.load_cv()
        
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
                is_valid, errors = self.contact_validator.validate_contact_data(contact_data)
                
                if not is_valid:
                    for error in errors:
                        flash(error, 'error')
                    return render_template("contact.html", cv=cv, title="Contacto")
                
                # Guardar datos
                cv['contact'] = contact_data
                if self.data_handler.save_cv(cv):
                    flash('Contacto guardado correctamente', 'success')
                    logger.info("Datos de contacto actualizados")
                    return redirect(url_for('contact'))
                else:
                    flash('Error al guardar los datos', 'error')
                    
            except Exception as e:
                logger.error(f"Error al guardar contacto: {e}")
                flash('Error inesperado al guardar', 'error')
        
        return render_template("contact.html", cv=cv, title="Contacto")
    
    def summary(self):
        """Gestión del resumen profesional"""
        cv = self.data_handler.load_cv()
        
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
                if self.data_handler.save_cv(cv):
                    flash('Resumen guardado correctamente', 'success')
                    logger.info("Resumen actualizado")
                    return redirect(url_for('summary'))
                else:
                    flash('Error al guardar el resumen', 'error')
                    
            except Exception as e:
                logger.error(f"Error al guardar resumen: {e}")
                flash('Error inesperado al guardar', 'error')
        
        return render_template("summary.html", cv=cv, title="Resumen")
    
    # ===== GESTIÓN DE SECCIONES =====
    
    def _get_section_list(self, cv, section):
        """Obtiene lista de items de una sección"""
        if section not in cv:
            cv[section] = []
        return cv[section]
    
    def list_items(self, section):
        """Lista items de una sección"""
        if section not in self.config.CV_SECTIONS:
            flash('Sección no válida', 'error')
            return redirect(url_for('index'))
        
        try:
            cv = self.data_handler.load_cv()
            items = list(enumerate(self._get_section_list(cv, section)))
            return render_template(
                "list.html", 
                section=section, 
                items=items, 
                title=section.capitalize()
            )
        except Exception as e:
            logger.error(f"Error al listar items de {section}: {e}")
            flash('Error al cargar los datos', 'error')
            return redirect(url_for('index'))
    
    def add_item(self, section):
        """Añade un item a una sección"""
        if section not in self.config.CV_SECTIONS:
            flash('Sección no válida', 'error')
            return redirect(url_for('index'))
        
        cv = self.data_handler.load_cv()
        item = {}
        
        if request.method == 'POST':
            try:
                # Recopilar datos del formulario
                fields = self.config.SECTION_FIELDS.get(section, [])
                
                for field in fields:
                    value = request.form.get(field, '').strip()
                    
                    # Procesar arrays (tags, tech)
                    if field in ('tags', 'tech'):
                        item[field] = [
                            v.strip() for v in value.split(',') 
                            if v.strip()
                        ]
                    else:
                        item[field] = value
                
                # Validar item
                is_valid, errors = ItemValidator.validate_item(section, item)
                
                if not is_valid:
                    for error in errors:
                        flash(error, 'error')
                    return render_template(
                        "edit_item.html", 
                        section=section, 
                        item=item, 
                        action="Añadir", 
                        title="Añadir"
                    )
                
                # Verificar límite de items
                if len(cv[section]) >= self.config.MAX_ITEMS_PER_SECTION:
                    flash(
                        f'Límite de {self.config.MAX_ITEMS_PER_SECTION} items alcanzado', 
                        'warning'
                    )
                    return redirect(url_for('list_items', section=section))
                
                # Añadir item
                cv[section].append(item)
                
                if self.data_handler.save_cv(cv):
                    flash('Item añadido correctamente', 'success')
                    logger.info(f"Item añadido a {section}")
                    return redirect(url_for('list_items', section=section))
                else:
                    flash('Error al guardar el item', 'error')
                    
            except Exception as e:
                logger.error(f"Error al añadir item a {section}: {e}")
                flash('Error inesperado al añadir', 'error')
        
        return render_template(
            "edit_item.html", 
            section=section, 
            item=item, 
            action="Añadir", 
            title="Añadir"
        )
    
    def edit_item(self, section, idx):
        """Edita un item existente"""
        if section not in self.config.CV_SECTIONS:
            flash('Sección no válida', 'error')
            return redirect(url_for('index'))
        
        cv = self.data_handler.load_cv()
        items_list = self._get_section_list(cv, section)
        
        # Validar índice
        if idx < 0 or idx >= len(items_list):
            flash('Item no encontrado', 'error')
            return redirect(url_for('list_items', section=section))
        
        if request.method == 'POST':
            try:
                item = items_list[idx]
                fields = self.config.SECTION_FIELDS.get(section, [])
                
                # Actualizar datos
                for field in fields:
                    value = request.form.get(field, '').strip()
                    
                    if field in ('tags', 'tech'):
                        item[field] = [
                            v.strip() for v in value.split(',') 
                            if v.strip()
                        ]
                    else:
                        item[field] = value
                
                # Validar
                is_valid, errors = ItemValidator.validate_item(section, item)
                
                if not is_valid:
                    for error in errors:
                        flash(error, 'error')
                    return render_template(
                        "edit_item.html", 
                        section=section, 
                        item=item, 
                        action="Editar", 
                        title="Editar"
                    )
                
                # Guardar
                if self.data_handler.save_cv(cv):
                    flash('Item actualizado correctamente', 'success')
                    logger.info(f"Item {idx} de {section} actualizado")
                    return redirect(url_for('list_items', section=section))
                else:
                    flash('Error al guardar cambios', 'error')
                    
            except Exception as e:
                logger.error(f"Error al editar item {idx} de {section}: {e}")
                flash('Error inesperado al editar', 'error')
        
        return render_template(
            "edit_item.html", 
            section=section, 
            item=items_list[idx], 
            action="Editar", 
            title="Editar"
        )
    
    def delete_item(self, section, idx):
        """Elimina un item"""
        if section not in self.config.CV_SECTIONS:
            flash('Sección no válida', 'error')
            return redirect(url_for('index'))
        
        try:
            cv = self.data_handler.load_cv()
            items_list = self._get_section_list(cv, section)
            
            if 0 <= idx < len(items_list):
                deleted_item = items_list.pop(idx)
                
                if self.data_handler.save_cv(cv):
                    flash('Item eliminado correctamente', 'success')
                    logger.info(f"Item {idx} eliminado de {section}")
                else:
                    flash('Error al eliminar el item', 'error')
            else:
                flash('Item no encontrado', 'error')
                
        except Exception as e:
            logger.error(f"Error al eliminar item {idx} de {section}: {e}")
            flash('Error inesperado al eliminar', 'error')
        
        return redirect(url_for('list_items', section=section))
    
    # ===== PERSONALIZACIÓN =====
    
    def customize(self):
        """Página de personalización del CV"""
        try:
            cv = self.data_handler.load_cv()
            templates = self.data_handler.load_templates()
            return render_template(
                "customize.html", 
                cv=cv, 
                templates=templates, 
                title="Personalizar CV"
            )
        except Exception as e:
            logger.error(f"Error en customize: {e}")
            flash('Error al cargar datos de personalización', 'error')
            return redirect(url_for('index'))
    
    def load_template(self, template_name):
        """Carga una plantilla guardada"""
        try:
            templates = self.data_handler.load_templates()
            
            if template_name in templates:
                return jsonify(templates[template_name])
            
            return jsonify({"error": "Plantilla no encontrada"}), 404
            
        except Exception as e:
            logger.error(f"Error al cargar plantilla {template_name}: {e}")
            return jsonify({"error": "Error al cargar plantilla"}), 500
    
    def save_template(self):
        """Guarda una plantilla de selección"""
        try:
            data = request.get_json()
            template_name = data.get("name", "").strip()
            
            if not template_name:
                return jsonify({"error": "Nombre de plantilla requerido"}), 400
            
            # Validar nombre
            if len(template_name) > 50:
                return jsonify({"error": "Nombre demasiado largo (máx. 50 caracteres)"}), 400
            
            templates = self.data_handler.load_templates()
            
            templates[template_name] = {
                "name": template_name,
                "description": data.get("description", ""),
                "selection": data.get("selection", {}),
                "created": data.get("created", "")
            }
            
            if self.data_handler.save_templates(templates):
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
    
    def delete_template(self, template_name):
        """Elimina una plantilla guardada"""
        try:
            templates = self.data_handler.load_templates()
            
            if template_name in templates:
                del templates[template_name]
                
                if self.data_handler.save_templates(templates):
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
    
    # ===== PREVIEW Y GENERACIÓN =====
    
    def _filter_cv_by_selection(self, cv, selection):
        """Filtra el CV según la selección"""
        filtered_cv = {
            "contact": cv.get("contact", {}),
            "summary": cv.get("summary", "") if selection.get("include_summary", True) else ""
        }
        
        for section in self.config.CV_SECTIONS:
            if section in selection and "selected" in selection[section]:
                original_items = cv.get(section, [])
                selected_indices = selection[section]["selected"]
                order = selection[section].get("order", list(range(len(selected_indices))))
                
                selected_items = []
                for pos in order:
                    if pos < len(selected_indices):
                        idx = selected_indices[pos]
                        if idx < len(original_items):
                            selected_items.append(original_items[idx])
                
                filtered_cv[section] = selected_items
            else:
                filtered_cv[section] = cv.get(section, [])
        
        return filtered_cv
    
    def _render_to_text(self, cv, fmt="md"):
        """Renderiza el CV a texto"""
        template_name = "cv.md.j2" if fmt == "md" else "cv.txt.j2"
        template = self.jinja_env.get_template(template_name)
        return template.render(**cv)
    
    def preview(self):
        """Vista previa del CV"""
        try:
            cv = self.data_handler.load_cv()
            cv = self.data_handler.dedup_otros(cv)
            fmt = request.args.get("fmt", "md")
            
            content = self._render_to_text(cv, fmt=fmt)
            
            return render_template("preview.html", content=content, title="Vista previa")
            
        except Exception as e:
            logger.error(f"Error en preview: {e}")
            flash('Error al generar vista previa', 'error')
            return redirect(url_for('index'))
    
    def preview_custom(self):
        """Vista previa con selección personalizada"""
        try:
            data = request.get_json()
            selection = data.get("selection", {})
            fmt = data.get("fmt", "md")
            
            cv = self.data_handler.load_cv()
            cv = self.data_handler.dedup_otros(cv)
            filtered_cv = self._filter_cv_by_selection(cv, selection)
            
            content = self._render_to_text(filtered_cv, fmt=fmt)
            
            return jsonify({"content": content})
            
        except Exception as e:
            logger.error(f"Error en preview_custom: {e}")
            return jsonify({"error": "Error al generar vista previa"}), 500
    
    def generate(self):
        """Genera el CV completo"""
        cv = self.data_handler.load_cv()
        cv = self.data_handler.dedup_otros(cv)
        fmt = "md"
        outname = "CV"
        outputs = []
        
        if request.method == 'POST':
            try:
                fmt = request.form.get("fmt", "md")
                outname = request.form.get("outname", "CV").strip()
                
                # Validar nombre de archivo
                if not outname or len(outname) > 100:
                    flash('Nombre de archivo inválido', 'error')
                    return render_template(
                        "generate.html", 
                        fmt=fmt, 
                        outname=outname, 
                        outputs=outputs, 
                        title="Generar"
                    )
                
                # Procesar selección si existe
                selection_data = request.form.get("selection_data")
                if selection_data:
                    try:
                        import json
                        selection = json.loads(selection_data)
                        cv = self._filter_cv_by_selection(cv, selection)
                    except:
                        pass
                
                content = self._render_to_text(cv, fmt=fmt)
                ext = ".md" if fmt == "md" else ".txt"
                outpath = self.config.OUT_DIR / f"{outname}{ext}"
                
                outpath.write_text(content, encoding="utf-8")
                outputs.append(outpath.name)
                
                flash('CV generado correctamente', 'success')
                logger.info(f"CV generado: {outpath.name}")
                
            except Exception as e:
                logger.error(f"Error al generar CV: {e}")
                flash('Error al generar el CV', 'error')
        
        return render_template(
            "generate.html", 
            fmt=fmt, 
            outname=outname, 
            outputs=outputs, 
            title="Generar"
        )
    
    def generate_custom(self):
        """Genera CV con selección personalizada"""
        try:
            data = request.get_json()
            selection = data.get("selection", {})
            fmt = data.get("fmt", "md")
            outname = data.get("outname", "CV_personalizado").strip()
            
            # Validar nombre
            if not outname or len(outname) > 100:
                return jsonify({"error": "Nombre de archivo inválido"}), 400
            
            cv = self.data_handler.load_cv()
            cv = self.data_handler.dedup_otros(cv)
            filtered_cv = self._filter_cv_by_selection(cv, selection)
            
            content = self._render_to_text(filtered_cv, fmt=fmt)
            ext = ".md" if fmt == "md" else ".txt"
            outpath = self.config.OUT_DIR / f"{outname}{ext}"
            
            outpath.write_text(content, encoding="utf-8")
            
            logger.info(f"CV personalizado generado: {outpath.name}")
            
            return jsonify({
                "success": True,
                "filename": outpath.name,
                "message": "CV generado correctamente"
            })
            
        except Exception as e:
            logger.error(f"Error al generar CV personalizado: {e}")
            return jsonify({"error": "Error al generar CV"}), 500
    
    def download(self, path):
        """Descarga un archivo generado"""
        from flask import send_from_directory
        
        try:
            return send_from_directory(
                self.config.OUT_DIR, 
                path, 
                as_attachment=True
            )
        except Exception as e:
            logger.error(f"Error al descargar {path}: {e}")
            flash('Archivo no encontrado', 'error')
            return redirect(url_for('generate'))
    
    # ===== MANEJADORES DE ERRORES =====
    
    def not_found(self, error):
        """Maneja error 404"""
        logger.warning(f"Página no encontrada: {request.url}")
        return render_template('404.html'), 404
    
    def internal_error(self, error):
        """Maneja error 500"""
        logger.error(f"Error interno: {error}")
        return render_template('500.html'), 500
    
    # ===== MÉTODOS DE EJECUCIÓN =====
    
    def run(self, **kwargs):
        """Ejecuta la aplicación"""
        self.app.run(**kwargs)


# ===== PUNTO DE ENTRADA =====

def create_app(config_name='development'):
    """
    Factory para crear la aplicación
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        Instancia de CVGeneratorApp
    """
    from app.config import get_config
    
    config_class = get_config(config_name)
    return CVGeneratorApp(config_class)


if __name__ == "__main__":
    # Crear y ejecutar aplicación
    app = create_app()
    
    print("=" * 50)
    print("CV GENERATOR - Generador de Currículums")
    print("=" * 50)
    print("Iniciando aplicación...")
    print(f"Accede a: http://{app.config.HOST}:{app.config.PORT}")
    print("Para cerrar: Ctrl+C")
    print("=" * 50)
    
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG
    )