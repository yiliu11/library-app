from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import requests
from .utils.logger import setup_logging
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

# Initialize external service clients
class ExternalServiceClient:
    @staticmethod
    def get_user_service_url():
        return Config.USER_SERVICE_URL

    @staticmethod
    def get_book_service_url():
        return Config.BOOK_SERVICE_URL

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Setup logging
    setup_logging(app)

    # Register blueprints
    from .routes.checkout_routes import checkout_bp
    app.register_blueprint(checkout_bp, url_prefix='/api/checkout')

    return app
