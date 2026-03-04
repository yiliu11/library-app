from flask import Flask
from .config import Config
from .extensions import db, migrate
from .errors import register_error_handlers
from .catalog import catalog_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(catalog_bp, url_prefix="/api/catalog")

    # Error handlers
    register_error_handlers(app)

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app
