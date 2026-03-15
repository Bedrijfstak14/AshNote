import os
import logging
from flask import Flask
from flask_migrate import Migrate
from app.config import Config
from app.models import db
from app.utils import is_admin
from app.extensions import csrf, limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def create_app(test_config=None):
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, "templates"),
        static_folder=os.path.join(basedir, "static"),
    )

    app.config.from_object(Config)
    Config.init_app(app)

    if test_config:
        app.config.update(test_config)

    # Extensions
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    # Security headers op elke response
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # Blueprints
    from app.auth import auth
    from app.admin import admin
    from app.cigars import cigars
    from app.api import api

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin)
    app.register_blueprint(cigars)
    app.register_blueprint(api)

    @app.context_processor
    def inject_is_admin():
        return {"is_admin": is_admin()}

    return app
