import os
from flask import Flask
from app.config import Config
from app.models import db
from app.utils import is_admin

def create_app():
    # Get the parent directory (where templates and static folders are)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Load configuration
    app.config.from_object(Config)
    Config.init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.auth import auth
    from app.admin import admin
    from app.cigars import cigars
    from app.api import api
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin)
    app.register_blueprint(cigars)
    app.register_blueprint(api)
    
    # Context processor for templates
    @app.context_processor
    def inject_is_admin():
        return {
            "is_admin": is_admin()
        }
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
