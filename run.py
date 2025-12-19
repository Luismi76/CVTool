#!/usr/bin/env python3
"""
Script de ejecución de CV Generator
Compatible con deployment en Render y desarrollo local
"""
import os
import sys
import webbrowser
import threading
import time

def open_browser(url, delay=2):
    """Abre el navegador después de un delay (solo en desarrollo local)"""
    time.sleep(delay)
    webbrowser.open(url)
    print(f"\n✅ Aplicación abierta en el navegador: {url}")

def main():
    """Función principal"""
    # Banner de bienvenida
    print("\n" + "=" * 60)
    print("  📄 CV GENERATOR - Generador de Currículums Profesional")
    print("=" * 60)
    print("\n🚀 Iniciando aplicación...")
    
    # Cargar configuración desde .env.local si existe
    try:
        from dotenv import load_dotenv
        if os.path.exists('.env.local'):
            load_dotenv('.env.local')
            print("   ✅ Configuración cargada desde .env.local")
    except ImportError:
        print("   ℹ️  python-dotenv no instalado")
    
    # Configurar entorno - RENDER necesita 0.0.0.0
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Si estamos en Render, usar 0.0.0.0, sino localhost
    is_render = os.environ.get('RENDER', False)
    host = '0.0.0.0' if is_render else os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"   Entorno: {env}")
    print(f"   Host: {host}")
    print(f"   Puerto: {port}")
    
    # Solo mostrar y abrir navegador si NO estamos en Render
    if not is_render:
        print(f"   URL: http://127.0.0.1:{port}")
        print(f"\n💡 La aplicación se abrirá automáticamente en tu navegador")
        print(f"   Si no se abre, accede manualmente a: http://127.0.0.1:{port}")
    else:
        print(f"   Ejecutando en Render en puerto {port}")
    
    print(f"\n⚠️  Para cerrar la aplicación, presiona Ctrl+C")
    print("=" * 60 + "\n")
    
    try:
        # Importar la aplicación
        from app import create_app
        
        # Crear instancia
        app_instance = create_app(env)
        
        # Abrir navegador solo en desarrollo local
        if not is_render:
            url = f"http://127.0.0.1:{port}"
            browser_thread = threading.Thread(
                target=open_browser, 
                args=(url,), 
                daemon=True
            )
            browser_thread.start()
        
        # Ejecutar aplicación
        app_instance.run(
            host=host,
            port=port,
            debug=(env == 'development' and not is_render),
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n\n✋ Aplicación cerrada por el usuario")
        print("¡Gracias por usar CV Generator!")
        sys.exit(0)
        
    except ImportError as e:
        print(f"\n❌ Error: Faltan dependencias necesarias")
        print(f"   Detalles: {e}")
        print(f"\n💡 Solución: Ejecuta 'pip install -r requirements.txt'")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print(f"\n💡 Si el problema persiste, revisa el archivo cv_generator.log")
        sys.exit(1)

if __name__ == "__main__":
    main()