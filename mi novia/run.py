#!/usr/bin/env python3
"""
Life Organizer - Aplicación de Salud y Productividad
Archivo principal para ejecutar la aplicación Flask
"""

from app import create_app
import os

# Crear la aplicación Flask
app = create_app()

if __name__ == '__main__':
    # Configuración para desarrollo
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("🏥 Life Organizer - Aplicación de Salud")
    print("=" * 50)
    print(f"🌐 Servidor iniciado en: http://localhost:{port}")
    print(f"🔧 Modo debug: {'Activado' if debug_mode else 'Desactivado'}")
    print("=" * 50)
    
    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
