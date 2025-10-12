"""
Validadores para datos de entrada del usuario
"""
import re
from typing import Any, Dict, List, Optional, Tuple


class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    pass


class Validator:
    """Clase base para validadores"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        if not email:
            return True, None
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email.strip()):
            return True, None
        return False, "Formato de email inválido"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
        if not phone:
            return True, None
        pattern = r'^[\d\s\-\+\(\)]{9,20}$'
        if re.match(pattern, phone.strip()):
            return True, None
        return False, "Formato de teléfono inválido (mínimo 9 dígitos)"
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        if not url:
            return True, None
        pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+$'
        if re.match(pattern, url.strip()):
            return True, None
        return False, "Formato de URL inválido"
    
    @staticmethod
    def validate_date_format(date_str: str) -> Tuple[bool, Optional[str]]:
        if not date_str:
            return True, None
        patterns = [
            r'^\d{4}-\d{2}$',
            r'^\d{4}$',
            r'^(Actual|Presente|Present|Current)$'
        ]
        date_str = date_str.strip()
        for pattern in patterns:
            if re.match(pattern, date_str, re.IGNORECASE):
                return True, None
        return False, "Formato de fecha inválido (use YYYY-MM, YYYY o 'Actual')"
    
    @staticmethod
    def validate_text_length(text: str, min_len: int = 0, max_len: int = 10000) -> Tuple[bool, Optional[str]]:
        if not text:
            if min_len > 0:
                return False, f"El texto debe tener al menos {min_len} caracteres"
            return True, None
        length = len(text.strip())
        if length < min_len:
            return False, f"El texto debe tener al menos {min_len} caracteres"
        if length > max_len:
            return False, f"El texto no puede exceder {max_len} caracteres"
        return True, None
    
    @staticmethod
    def sanitize_string(text: str) -> str:
        if not text:
            return ""
        text = " ".join(text.split())
        dangerous_chars = ['<', '>', '{', '}', '\\x00']
        for char in dangerous_chars:
            text = text.replace(char, '')
        return text.strip()


class ContactValidator(Validator):
    """Validador específico para datos de contacto"""
    
    @classmethod
    def validate_contact_data(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        name = data.get("name", "").strip()
        if not name:
            errors.append("El nombre es obligatorio")
        elif len(name) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres")
        
        email = data.get("email", "").strip()
        if not email:
            errors.append("El email es obligatorio")
        else:
            is_valid, error = cls.validate_email(email)
            if not is_valid:
                errors.append(error)
        
        phone = data.get("phone", "").strip()
        if phone:
            is_valid, error = cls.validate_phone(phone)
            if not is_valid:
                errors.append(error)
        
        links = data.get("links", [])
        if isinstance(links, list):
            for i, link in enumerate(links, 1):
                is_valid, error = cls.validate_url(link)
                if not is_valid:
                    errors.append(f"Link {i}: {error}")
        
        return len(errors) == 0, errors


class ItemValidator(Validator):
    """Validador para items de secciones del CV"""
    
    @classmethod
    def validate_item(cls, section: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Valida un item según su sección - SIN VALIDACIÓN"""
        return True, []