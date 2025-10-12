/**
 * Tour Guiado de CV Generator
 * Sistema de tutorial interactivo para nuevos usuarios
 */

class CVTour {
    constructor() {
        this.tourKey = 'cvgenerator_tour_completed';
        this.intro = null;
    }

    /**
     * Inicializa el tour si es la primera vez del usuario
     */
    init() {
        // Esperar a que el DOM esté completamente cargado
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.checkAndStart());
        } else {
            this.checkAndStart();
        }
    }

    /**
     * Verifica si debe mostrar el tour
     */
    checkAndStart() {
        const tourCompleted = localStorage.getItem(this.tourKey);
        
        // Si es la primera vez (no hay marca en localStorage), mostrar tour
        if (!tourCompleted && this.isHomePage()) {
            // Pequeño delay para que la página cargue completamente
            setTimeout(() => {
                this.showWelcomeDialog();
            }, 800);
        }
    }

    /**
     * Verifica si estamos en la página principal
     */
    isHomePage() {
        return window.location.pathname === '/' || window.location.pathname === '/index';
    }

    /**
     * Muestra diálogo de bienvenida
     */
    showWelcomeDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'tour-welcome-dialog';
        dialog.innerHTML = `
            <div class="tour-welcome-content">
                <div class="tour-icon">📄</div>
                <h2>Bienvenido a CV Generator</h2>
                <p>Tu herramienta para crear currículums profesionales personalizados.</p>
                <p style="margin-top: 15px;">¿Quieres un recorrido rápido de 2 minutos?</p>
                <div class="tour-welcome-buttons">
                    <button id="tour-start-btn" class="btn btn-primary">
                        🚀 Sí, empezar
                    </button>
                    <button id="tour-skip-btn" class="btn btn-secondary">
                        Ahora no
                    </button>
                </div>
                <label class="tour-checkbox">
                    <input type="checkbox" id="tour-dont-show"> No volver a mostrar
                </label>
            </div>
        `;

        document.body.appendChild(dialog);

        // Event listeners
        document.getElementById('tour-start-btn').addEventListener('click', () => {
            document.body.removeChild(dialog);
            this.startTour();
        });

        document.getElementById('tour-skip-btn').addEventListener('click', () => {
            const dontShow = document.getElementById('tour-dont-show').checked;
            if (dontShow) {
                localStorage.setItem(this.tourKey, 'skipped');
            }
            document.body.removeChild(dialog);
        });
    }

    /**
     * Inicia el tour guiado
     */
    startTour() {
        this.intro = introJs();

        this.intro.setOptions({
            nextLabel: 'Siguiente',
            prevLabel: 'Anterior',
            skipLabel: 'Saltar',
            doneLabel: 'Finalizar',
            showProgress: true,
            showBullets: true,
            exitOnOverlayClick: false,
            disableInteraction: true,
            scrollToElement: true,
            scrollPadding: 30,
            steps: this.getTourSteps()
        });

        // Cuando termina el tour
        this.intro.oncomplete(() => {
            localStorage.setItem(this.tourKey, 'completed');
            this.showCompletionMessage();
        });

        // Si el usuario cancela
        this.intro.onexit(() => {
            const currentStep = this.intro._currentStep;
            const totalSteps = this.getTourSteps().length;
            if (currentStep < totalSteps - 1) {
                // No marcar como completado si no terminó
                console.log('Tour cancelado en paso ' + (currentStep + 1) + ' de ' + totalSteps);
            }
        });

        this.intro.start();
    }

    /**
     * Define los pasos del tour
     */
    getTourSteps() {
        const steps = [
            {
                intro: `
                    <div class="tour-step-intro">
                        <h2>📄 Bienvenido a CV Generator</h2>
                        <p>Tu herramienta para crear currículums profesionales adaptados a cada oferta.</p>
                        <p><strong>Duración:</strong> 2 minutos</p>
                    </div>
                `
            }
        ];

        // Añadir pasos solo si los elementos existen
        const contactLink = document.querySelector('a[href="/contact"]');
        if (contactLink) {
            steps.push({
                element: contactLink,
                intro: `
                    <h3>📧 Paso 1: Contacto</h3>
                    <p>Empieza configurando tu información básica:</p>
                    <ul>
                        <li>Nombre y email</li>
                        <li>Teléfono y ubicación</li>
                        <li>Enlaces (LinkedIn, GitHub)</li>
                    </ul>
                `,
                position: 'bottom'
            });
        }

        const summaryLink = document.querySelector('a[href="/summary"]');
        if (summaryLink) {
            steps.push({
                element: summaryLink,
                intro: `
                    <h3>📝 Paso 2: Resumen</h3>
                    <p>Un breve párrafo sobre tu perfil profesional.</p>
                    <p><em>Consejo: Adáptalo según el puesto</em></p>
                `,
                position: 'bottom'
            });
        }

        const sectionsDropdown = document.querySelector('.nav-dropdown');
        if (sectionsDropdown) {
            steps.push({
                element: sectionsDropdown,
                intro: `
                    <h3>📋 Paso 3: Añadir Información</h3>
                    <p>Completa las secciones de tu CV:</p>
                    <ul>
                        <li>Habilidades</li>
                        <li>Experiencia</li>
                        <li>Proyectos</li>
                        <li>Educación</li>
                        <li>Cursos</li>
                    </ul>
                `,
                position: 'bottom'
            });
        }

        const customizeLink = document.querySelector('a[href="/personalizar"]');
        if (customizeLink) {
            steps.push({
                element: customizeLink,
                intro: `
                    <h3>🎯 Paso 4: Personalizar</h3>
                    <p><strong>¡Lo más importante!</strong></p>
                    <p>Adapta tu CV para cada oferta:</p>
                    <ul>
                        <li>Selecciona elementos relevantes</li>
                        <li>Reordena por importancia</li>
                        <li>Guarda como plantilla</li>
                    </ul>
                `,
                position: 'bottom'
            });
        }

        const generateLink = document.querySelector('a[href="/generar"]');
        if (generateLink) {
            steps.push({
                element: generateLink.parentElement || generateLink,
                intro: `
                    <h3>📄 Paso 5: Generar y Descargar</h3>
                    <p>Descarga tu CV en dos formatos:</p>
                    <ul>
                        <li><strong>Markdown:</strong> Para web/GitHub</li>
                        <li><strong>Texto:</strong> Para portales de empleo</li>
                    </ul>
                `,
                position: 'bottom'
            });
        }

        steps.push({
            intro: `
                <div class="tour-step-intro">
                    <h2>🎉 ¡Listo!</h2>
                    <p>Ya conoces las funcionalidades principales.</p>
                    <div style="margin-top: 20px; text-align: left;">
                        <strong>Próximos pasos:</strong>
                        <ol>
                            <li>Configura tu contacto</li>
                            <li>Añade experiencia</li>
                            <li>Personaliza según la oferta</li>
                            <li>¡Descarga tu CV!</li>
                        </ol>
                    </div>
                    <p style="margin-top: 20px;"><strong>💪 ¡Mucha suerte!</strong></p>
                </div>
            `
        });

        return steps;
    }

    /**
     * Muestra mensaje de completación
     */
    showCompletionMessage() {
        if (typeof showNotification === 'function') {
            showNotification('¡Tour completado! Ya puedes empezar a crear tu CV 🎉', 'success', 5000);
        } else {
            alert('¡Tour completado! Ya puedes empezar a crear tu CV 🎉');
        }
    }

    /**
     * Reinicia el tour (para botón de ayuda)
     */
    restart() {
        localStorage.removeItem(this.tourKey);
        
        // Si no estamos en la página principal, redirigir
        if (!this.isHomePage()) {
            window.location.href = '/';
            return;
        }
        
        this.startTour();
    }
}

// Crear instancia global
window.cvTour = new CVTour();

// Inicializar automáticamente
window.cvTour.init();

// Exportar para uso manual
window.startCVTour = function() {
    window.cvTour.restart();
};