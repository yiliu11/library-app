from flask import Flask
from .config import Config
from .extensions import db, migrate
from .errors import register_error_handlers
from .users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    app.register_blueprint(users_bp, url_prefix="/api/users")

    # Errors
    register_error_handlers(app)

    # Health
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app
