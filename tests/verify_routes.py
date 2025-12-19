import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

def test_routes():
    print("🚀 Iniciando verificación de rutas...")
    app = create_app('development')
    client = app.test_client()
    
    routes_to_test = [
        ('/', 200),
        ('/acerca', 200),
        ('/contact', 200),
        ('/summary', 200),
        ('/personalizar', 200),
        ('/preview', 200),
        ('/skills', 200), # List items
    ]
    
    all_passed = True
    
    for route, expected_code in routes_to_test:
        try:
            response = client.get(route)
            if response.status_code == expected_code:
                print(f"✅ Route {route}: OK ({response.status_code})")
            else:
                print(f"❌ Route {route}: FAILED (Expected {expected_code}, got {response.status_code})")
                all_passed = False
        except Exception as e:
            print(f"❌ Route {route}: ERROR ({str(e)})")
            all_passed = False
            
    if all_passed:
        print("\n✨ Todas las rutas verificadas correctamente.")
        sys.exit(0)
    else:
        print("\n💥 Fallaron algunas verificaciones.")
        sys.exit(1)

if __name__ == "__main__":
    test_routes()
