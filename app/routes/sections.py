from flask import render_template, request, redirect, url_for, flash, current_app
from app.routes import sections_bp
from app.validators import ItemValidator
import logging

logger = logging.getLogger(__name__)

def _get_section_list(cv, section):
    """Obtiene lista de items de una sección"""
    if section not in cv:
        cv[section] = []
    return cv[section]

@sections_bp.route('/<section>')
def list_items(section):
    """Lista items de una sección"""
    if section not in current_app.config['CV_SECTIONS']:
        flash('Sección no válida', 'error')
        return redirect(url_for('main.index'))
    
    try:
        cv = current_app.data_handler.load_cv()
        items = list(enumerate(_get_section_list(cv, section)))
        return render_template(
            "list.html", 
            section=section, 
            items=items, 
            title=section.capitalize()
        )
    except Exception as e:
        logger.error(f"Error al listar items de {section}: {e}")
        flash('Error al cargar los datos', 'error')
        return redirect(url_for('main.index'))

@sections_bp.route('/<section>/add', methods=['GET', 'POST'])
def add_item(section):
    """Añade un item a una sección"""
    if section not in current_app.config['CV_SECTIONS']:
        flash('Sección no válida', 'error')
        return redirect(url_for('main.index'))
    
    cv = current_app.data_handler.load_cv()
    item = {}
    
    if request.method == 'POST':
        try:
            # Recopilar datos del formulario
            fields = current_app.config['SECTION_FIELDS'].get(section, [])
            
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
            if len(cv[section]) >= current_app.config['MAX_ITEMS_PER_SECTION']:
                flash(
                    f'Límite de {current_app.config["MAX_ITEMS_PER_SECTION"]} items alcanzado', 
                    'warning'
                )
                return redirect(url_for('sections.list_items', section=section))
            
            # Añadir item
            cv[section].append(item)
            
            if current_app.data_handler.save_cv(cv):
                flash('Item añadido correctamente', 'success')
                logger.info(f"Item añadido a {section}")
                return redirect(url_for('sections.list_items', section=section))
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

@sections_bp.route('/<section>/edit/<int:idx>', methods=['GET', 'POST'])
def edit_item(section, idx):
    """Edita un item existente"""
    if section not in current_app.config['CV_SECTIONS']:
        flash('Sección no válida', 'error')
        return redirect(url_for('main.index'))
    
    cv = current_app.data_handler.load_cv()
    items_list = _get_section_list(cv, section)
    
    # Validar índice
    if idx < 0 or idx >= len(items_list):
        flash('Item no encontrado', 'error')
        return redirect(url_for('sections.list_items', section=section))
    
    if request.method == 'POST':
        try:
            item = items_list[idx]
            fields = current_app.config['SECTION_FIELDS'].get(section, [])
            
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
            if current_app.data_handler.save_cv(cv):
                flash('Item actualizado correctamente', 'success')
                logger.info(f"Item {idx} de {section} actualizado")
                return redirect(url_for('sections.list_items', section=section))
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

@sections_bp.route('/<section>/delete/<int:idx>')
def delete_item(section, idx):
    """Elimina un item"""
    if section not in current_app.config['CV_SECTIONS']:
        flash('Sección no válida', 'error')
        return redirect(url_for('main.index'))
    
    try:
        cv = current_app.data_handler.load_cv()
        items_list = _get_section_list(cv, section)
        
        if 0 <= idx < len(items_list):
            deleted_item = items_list.pop(idx)
            
            if current_app.data_handler.save_cv(cv):
                flash('Item eliminado correctamente', 'success')
                logger.info(f"Item {idx} eliminado de {section}")
            else:
                flash('Error al eliminar el item', 'error')
        else:
            flash('Item no encontrado', 'error')
            
    except Exception as e:
        logger.error(f"Error al eliminar item {idx} de {section}: {e}")
        flash('Error inesperado al eliminar', 'error')
    
    return redirect(url_for('sections.list_items', section=section))
