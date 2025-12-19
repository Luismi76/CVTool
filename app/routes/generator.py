from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, send_from_directory, current_app
from app.routes import generator_bp
import logging
import json
from xhtml2pdf import pisa
from io import BytesIO

logger = logging.getLogger(__name__)

def _filter_cv_by_selection(cv, selection):
    """Filtra el CV según la selección"""
    filtered_cv = {
        "contact": cv.get("contact", {}),
        "summary": cv.get("summary", "") if selection.get("include_summary", True) else ""
    }
    
    for section in current_app.config['CV_SECTIONS']:
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

def _render_to_text(cv, fmt="md"):
    """Renderiza el CV a texto"""
    template_name = "cv.md.j2" if fmt == "md" else "cv.txt.j2"
    # Accedemos a jinja_env que hemos adjuntado a la app
    template = current_app.jinja_env.get_template(template_name)
    return template.render(**cv)

def _render_cv_html_for_pdf(cv):
    """Renderiza el CV como HTML optimizado para PDF"""
    return render_template('cv_pdf_template.j2', cv=cv)

@generator_bp.route('/preview')
def preview():
    """Vista previa del CV"""
    try:
        cv = current_app.data_handler.load_cv()
        cv = current_app.data_handler.dedup_otros(cv)
        fmt = request.args.get("fmt", "md")
        
        content = _render_to_text(cv, fmt=fmt)
        
        return render_template("preview.html", content=content, title="Vista previa")
        
    except Exception as e:
        logger.error(f"Error en preview: {e}")
        flash('Error al generar vista previa', 'error')
        return redirect(url_for('main.index'))

@generator_bp.route('/preview/personalizada', methods=['POST'])
def preview_custom():
    """Vista previa con selección personalizada"""
    try:
        data = request.get_json()
        selection = data.get("selection", {})
        fmt = data.get("fmt", "md")
        
        cv = current_app.data_handler.load_cv()
        cv = current_app.data_handler.dedup_otros(cv)
        filtered_cv = _filter_cv_by_selection(cv, selection)
        
        content = _render_to_text(filtered_cv, fmt=fmt)
        
        return jsonify({"content": content})
        
    except Exception as e:
        logger.error(f"Error en preview_custom: {e}")
        return jsonify({"error": "Error al generar vista previa"}), 500

@generator_bp.route('/generar', methods=['GET', 'POST'])
def generate():
    """Genera el CV completo (Redirige a personalizar si es GET directo, o procesa POST)"""
    if request.method == 'GET':
         return redirect(url_for('personalization.customize'))

    # Si es POST, mantenemos la logica original aunque customize la usa via AJAX normalmente
    # Pero aqui parece que generate.html existe para un formulario clasico?
    # En el codigo original app_refactored.py linea 117 estaba comentado y luego redefinido en linea 120 para redirigir
    # Mantendremos la redireccion para GET, y procesado simple para POST si fuese necesario, 
    # pero el frontend parece usar generate_custom via fetch o generate_pdf.
    # Por compatibilidad con 'generate.html' si se usa:
    
    cv = current_app.data_handler.load_cv()
    cv = current_app.data_handler.dedup_otros(cv)
    fmt = "md"
    outname = "CV"
    outputs = []
    
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
                cv = _filter_cv_by_selection(cv, selection)
            except:
                pass
        
        content = _render_to_text(cv, fmt=fmt)
        ext = ".md" if fmt == "md" else ".txt"
        outpath = current_app.config_obj.OUT_DIR / f"{outname}{ext}"
        
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

@generator_bp.route('/generar/pdf', methods=['GET', 'POST'])
def generate_pdf():
    """Genera el CV en formato PDF"""
    try:
        cv = current_app.data_handler.load_cv()
        cv = current_app.data_handler.dedup_otros(cv)
        
        # Procesar selección si existe
        selection_data = request.args.get("selection_data") or request.form.get("selection_data")
        if selection_data:
            try:
                import json
                selection = json.loads(selection_data)
                cv = _filter_cv_by_selection(cv, selection)
            except:
                pass
        
        # Renderizar HTML para PDF
        html_content = _render_cv_html_for_pdf(cv)
        
        # Generar PDF
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
        
        if pisa_status.err:
            flash('Error al generar el PDF', 'error')
            return redirect(url_for('personalization.customize'))
        
        # Preparar descarga
        pdf_buffer.seek(0)
        outname = request.args.get("outname", "CV").strip() or "CV"
        
        logger.info(f"PDF generado: {outname}.pdf")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{outname}.pdf'
        )
        
    except Exception as e:
        logger.error(f"Error al generar PDF: {e}")
        flash('Error inesperado al generar el PDF', 'error')
        return redirect(url_for('personalization.customize'))

@generator_bp.route('/generar/personalizado', methods=['POST'])
def generate_custom():
    """Genera CV con selección personalizada"""
    try:
        data = request.get_json()
        selection = data.get("selection", {})
        fmt = data.get("fmt", "md")
        outname = data.get("outname", "CV_personalizado").strip()
        
        # Validar nombre
        if not outname or len(outname) > 100:
            return jsonify({"error": "Nombre de archivo inválido"}), 400
        
        cv = current_app.data_handler.load_cv()
        cv = current_app.data_handler.dedup_otros(cv)
        filtered_cv = _filter_cv_by_selection(cv, selection)
        
        content = _render_to_text(filtered_cv, fmt=fmt)
        ext = ".md" if fmt == "md" else ".txt"
        outpath = current_app.config_obj.OUT_DIR / f"{outname}{ext}"
        
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

@generator_bp.route('/download/<path:path>')
def download(path):
    """Descarga un archivo generado"""
    try:
        return send_from_directory(
            current_app.config_obj.OUT_DIR, 
            path, 
            as_attachment=True
        )
    except Exception as e:
        logger.error(f"Error al descargar {path}: {e}")
        flash('Archivo no encontrado', 'error')
        return redirect(url_for('personalization.customize'))
