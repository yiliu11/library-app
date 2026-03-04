from flask import Flask
from .config import Config
from .extensions import db, migrate
from .errors import register_error_handlers
from .checkout import checkout_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprints
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")

    # errors
    register_error_handlers(app)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app
