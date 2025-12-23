// JavaScript principal para CV Generator
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 CV Generator cargado correctamente');

    // Inicializar componentes
    initializeNavigation();
    initializeTheme();
    initializeAnimations();
    initializeNotifications();
    initializeFormValidation();
});

// ===== NAVEGACIÓN =====
function initializeNavigation() {
    // Marcar enlace activo
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link[href]');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.background = '#f8f9fa';
            link.style.color = '#667eea';
        }
    });

    // Navegación móvil mejorada
    const navContainer = document.querySelector('.nav-container');
    const navMenu = document.querySelector('.nav-menu');

    // Crear botón de menú móvil si es necesario
    if (window.innerWidth <= 768) {
        createMobileMenu();
    }

    // Redimensionar ventana
    window.addEventListener('resize', () => {
        if (window.innerWidth <= 768) {
            if (!document.querySelector('.nav-toggle')) {
                createMobileMenu();
            }
        } else {
            const toggle = document.querySelector('.nav-toggle');
            if (toggle) {
                toggle.remove();
                navMenu.style.display = 'flex';
            }
        }
    });
}

function createMobileMenu() {
    const navContainer = document.querySelector('.nav-container');
    const navMenu = document.querySelector('.nav-menu');

    // Crear botón toggle si no existe
    if (!document.querySelector('.nav-toggle')) {
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'nav-toggle';
        toggleBtn.innerHTML = '☰';
        toggleBtn.style.cssText = `
            background: none;
            border: none;
            font-size: 1.5em;
            color: #2c3e50;
            cursor: pointer;
            padding: 5px;
        `;

        navContainer.appendChild(toggleBtn);

        // Toggle functionality
        toggleBtn.addEventListener('click', () => {
            const isVisible = navMenu.style.display === 'flex';
            navMenu.style.display = isVisible ? 'none' : 'flex';
            toggleBtn.innerHTML = isVisible ? '☰' : '✕';
        });

        // Inicializar como oculto en móvil
        navMenu.style.display = 'none';
    }
}

// ===== TEMAS =====
function initializeTheme() {
    const savedTheme = localStorage.getItem('cv_theme') || 'default';
    setTheme(savedTheme);
}

window.setTheme = function (themeName) {
    // Limpiar clases de tema existentes
    document.body.classList.remove('theme-corporate', 'theme-creative');

    // Aplicar nuevo tema si no es default
    if (themeName !== 'default') {
        document.body.classList.add(`theme-${themeName}`);
    }

    // Guardar preferencia
    localStorage.setItem('cv_theme', themeName);

    // Notificar cambio (opcional)
    if (typeof console !== 'undefined') {
        console.log(`🎨 Tema cambiado a: ${themeName}`);
    }
};

// ===== ANIMACIONES =====
function initializeAnimations() {
    // Observer para animaciones de entrada
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');

                // Animación especial para contadores
                if (entry.target.classList.contains('stat-number')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, observerOptions);

    // Observar elementos con animación
    document.querySelectorAll('.fade-in, .stat-number, .feature-card').forEach(el => {
        observer.observe(el);
    });

    // Efecto de escritura para títulos
    const titleElements = document.querySelectorAll('[data-typewriter]');
    titleElements.forEach(el => {
        typeWriter(el, el.textContent, 100);
    });
}

function animateCounter(element) {
    const target = parseInt(element.textContent) || 0;
    const duration = 1500;
    const step = target / (duration / 16);
    let current = 0;

    element.textContent = '0';

    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

function typeWriter(element, text, speed = 100) {
    element.textContent = '';
    let i = 0;

    const timer = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(timer);
        }
    }, speed);
}

// ===== NOTIFICACIONES =====
function initializeNotifications() {
    // Función global para mostrar notificaciones
    window.showNotification = function (message, type = 'success', duration = 4000) {
        // Remover notificaciones existentes
        document.querySelectorAll('.notification').forEach(n => n.remove());

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;

        // Crear contenido de la notificación
        const content = document.createElement('div');
        content.style.cssText = 'display: flex; align-items: center; gap: 10px;';

        const icon = getNotificationIcon(type);
        const text = document.createElement('span');
        text.textContent = message;

        content.appendChild(icon);
        content.appendChild(text);
        notification.appendChild(content);

        // Añadir botón de cerrar
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '✕';
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: inherit;
            font-size: 1.2em;
            cursor: pointer;
            margin-left: 10px;
            opacity: 0.7;
            transition: opacity 0.3s ease;
        `;
        closeBtn.addEventListener('click', () => removeNotification(notification));
        closeBtn.addEventListener('mouseenter', () => closeBtn.style.opacity = '1');
        closeBtn.addEventListener('mouseleave', () => closeBtn.style.opacity = '0.7');

        content.appendChild(closeBtn);

        document.body.appendChild(notification);

        // Mostrar con animación
        setTimeout(() => notification.classList.add('show'), 100);

        // Auto-ocultar
        setTimeout(() => removeNotification(notification), duration);

        return notification;
    };

    // Función auxiliar para iconos
    function getNotificationIcon(type) {
        const icon = document.createElement('span');
        icon.style.fontSize = '1.2em';

        switch (type) {
            case 'success':
                icon.textContent = '✅';
                break;
            case 'error':
                icon.textContent = '❌';
                break;
            case 'info':
                icon.textContent = 'ℹ️';
                break;
            case 'warning':
                icon.textContent = '⚠️';
                break;
            default:
                icon.textContent = '📢';
        }

        return icon;
    }

    function removeNotification(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
}

// ===== VALIDACIÓN DE FORMULARIOS =====
function initializeFormValidation() {
    // Validación en tiempo real
    const inputs = document.querySelectorAll('input[required], textarea[required]');

    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => clearFieldError(input));
    });

    // Validación al enviar formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
                showNotification('Por favor, corrige los errores en el formulario', 'error');
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name || 'Campo';
    let isValid = true;
    let message = '';

    // Validaciones básicas
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = `${fieldName} es obligatorio`;
    } else if (field.type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Formato de email inválido';
    } else if (field.type === 'tel' && value && !isValidPhone(value)) {
        isValid = false;
        message = 'Formato de teléfono inválido';
    } else if (field.minLength && value.length < field.minLength) {
        isValid = false;
        message = `Mínimo ${field.minLength} caracteres`;
    }

    showFieldValidation(field, isValid, message);
    return isValid;
}

function showFieldValidation(field, isValid, message) {
    // Remover validación anterior
    clearFieldError(field);

    if (!isValid) {
        field.style.borderColor = '#dc3545';
        field.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';

        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.style.cssText = `
            color: #dc3545;
            font-size: 0.8em;
            margin-top: 5px;
            display: flex;
            align-items: center;
            gap: 5px;
        `;
        errorDiv.innerHTML = `<span>⚠️</span> ${message}`;

        field.parentNode.appendChild(errorDiv);
    } else if (field.value.trim()) {
        field.style.borderColor = '#28a745';
        field.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
    }
}

function clearFieldError(field) {
    field.style.borderColor = '#e9ecef';
    field.style.boxShadow = 'none';

    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function validateForm(form) {
    const requiredFields = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    return isValid;
}

// ===== UTILIDADES =====
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone) {
    return /^[\d\s\-\+\(\)]{9,}$/.test(phone);
}

// Función para loading states
window.showLoading = function (element, text = 'Cargando...') {
    const original = element.innerHTML;
    element.innerHTML = `<span>⏳</span> ${text}`;
    element.disabled = true;

    return function () {
        element.innerHTML = original;
        element.disabled = false;
    };
};

// Función para copiar al portapapeles
window.copyToClipboard = function (text, successMessage = 'Copiado al portapapeles') {
    navigator.clipboard.writeText(text).then(() => {
        showNotification(successMessage, 'success', 2000);
    }).catch(() => {
        showNotification('Error al copiar', 'error');
    });
};

// Debug info
console.log('📱 Dispositivo:', window.innerWidth <= 768 ? 'Móvil' : 'Escritorio');
console.log('🎨 CSS personalizado cargado');
console.log('⚡ JavaScript inicializado correctamente');