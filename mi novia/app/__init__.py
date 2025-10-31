from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

def create_app():
    """Factory function para crear la aplicación Flask"""
    # Obtener el directorio base del proyecto
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///life_organizer.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    from app.models import db
    db.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
    
    return app
