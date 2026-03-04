from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
import logging
import requests
from .utils.logger import setup_logging
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    mail.init_app(app)

    # Setup logging
    setup_logging(app)

    # Register blueprints
    from .routes.notification_routes import notification_bp
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')

    return app
