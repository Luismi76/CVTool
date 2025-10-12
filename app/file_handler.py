"""
Utilidades para manejo seguro de archivos JSON
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class FileHandler:
    """Maneja operaciones de lectura/escritura de archivos de forma segura"""
    
    @staticmethod
    def read_json(file_path: Path, default: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Lee un archivo JSON de forma segura
        
        Args:
            file_path: Ruta al archivo JSON
            default: Valor por defecto si el archivo no existe o hay error
            
        Returns:
            Diccionario con los datos del archivo o valor por defecto
        """
        if default is None:
            default = {}
            
        try:
            if not file_path.exists():
                logger.info(f"Archivo no encontrado: {file_path}. Usando valores por defecto.")
                return default
                
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Archivo leído correctamente: {file_path}")
                return data
                
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON en {file_path}: {e}")
            return default
            
        except Exception as e:
            logger.error(f"Error inesperado al leer {file_path}: {e}")
            return default
    
    @staticmethod
    def write_json(file_path: Path, data: Dict[str, Any], backup: bool = True) -> bool:
        """
        Escribe datos en un archivo JSON de forma segura
        
        Args:
            file_path: Ruta al archivo JSON
            data: Datos a escribir
            backup: Si True, crea backup antes de escribir
            
        Returns:
            True si la escritura fue exitosa, False en caso contrario
        """
        try:
            # Crear backup si el archivo existe
            if backup and file_path.exists():
                backup_path = FileHandler._create_backup(file_path)
                logger.debug(f"Backup creado: {backup_path}")
            
            # Escribir archivo temporal primero
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Mover archivo temporal al destino final
            temp_path.replace(file_path)
            logger.info(f"Archivo guardado correctamente: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al escribir archivo {file_path}: {e}")
            return False
    
    @staticmethod
    def _create_backup(file_path: Path) -> Path:
        """
        Crea un backup del archivo con timestamp
        
        Args:
            file_path: Ruta al archivo original
            
        Returns:
            Ruta al archivo de backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = file_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        backup_path = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
        
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            logger.warning(f"No se pudo crear backup: {e}")
            return file_path
    
    @staticmethod
    def validate_json_structure(data: Dict[str, Any], schema: Dict[str, type]) -> bool:
        """
        Valida la estructura básica de un diccionario
        
        Args:
            data: Datos a validar
            schema: Esquema esperado {clave: tipo}
            
        Returns:
            True si la estructura es válida
        """
        try:
            for key, expected_type in schema.items():
                if key not in data:
                    logger.warning(f"Clave faltante en validación: {key}")
                    return False
                    
                if not isinstance(data[key], expected_type):
                    logger.warning(
                        f"Tipo incorrecto para {key}: "
                        f"esperado {expected_type}, obtenido {type(data[key])}"
                    )
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error en validación: {e}")
            return False


class CVDataHandler:
    """Maneja específicamente los datos del CV"""
    
    DEFAULT_CV_STRUCTURE = {
        "contact": {"links": []},
        "summary": "",
        "skills": [],
        "experience": [],
        "projects": [],
        "education": [],
        "courses": [],
        "otros": []
    }
    
    def __init__(self, cv_file: Path, templates_file: Path):
        """
        Inicializa el manejador de datos del CV
        
        Args:
            cv_file: Ruta al archivo cv.json
            templates_file: Ruta al archivo templates.json
        """
        self.cv_file = cv_file
        self.templates_file = templates_file
        self.file_handler = FileHandler()
    
    def load_cv(self) -> Dict[str, Any]:
        """Carga los datos del CV"""
        return self.file_handler.read_json(
            self.cv_file, 
            default=self.DEFAULT_CV_STRUCTURE.copy()
        )
    
    def save_cv(self, cv_data: Dict[str, Any]) -> bool:
        """
        Guarda los datos del CV después de validar
        
        Args:
            cv_data: Datos del CV a guardar
            
        Returns:
            True si se guardó correctamente
        """
        # Validación básica
        if not isinstance(cv_data, dict):
            logger.error("Los datos del CV deben ser un diccionario")
            return False
        
        # Asegurar estructura mínima
        for key in self.DEFAULT_CV_STRUCTURE:
            if key not in cv_data:
                cv_data[key] = self.DEFAULT_CV_STRUCTURE[key]
        
        return self.file_handler.write_json(self.cv_file, cv_data)
    
    def load_templates(self) -> Dict[str, Any]:
        """Carga las plantillas guardadas"""
        return self.file_handler.read_json(self.templates_file, default={})
    
    def save_templates(self, templates_data: Dict[str, Any]) -> bool:
        """
        Guarda las plantillas
        
        Args:
            templates_data: Plantillas a guardar
            
        Returns:
            True si se guardó correctamente
        """
        if not isinstance(templates_data, dict):
            logger.error("Las plantillas deben ser un diccionario")
            return False
            
        return self.file_handler.write_json(self.templates_file, templates_data)
    
    def dedup_otros(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Elimina duplicados de la sección 'otros'
        
        Args:
            cv_data: Datos del CV
            
        Returns:
            CV con duplicados eliminados
        """
        otros = cv_data.get("otros", [])
        seen = set()
        cleaned = []
        
        for item in otros:
            # Crear signature única del item
            signature = (
                (item.get("title") or "").strip(),
                (item.get("institution") or item.get("company") or "").strip(),
                (item.get("periodo") or item.get("start") or "").strip()
            )
            
            if signature not in seen:
                seen.add(signature)
                cleaned.append(item)
        
        cv_data["otros"] = cleaned
        return cv_data


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)