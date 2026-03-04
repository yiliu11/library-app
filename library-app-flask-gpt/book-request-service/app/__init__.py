from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate is aware
    from . import models  

    # Register routes
    from .routes import request_bp
    app.register_blueprint(request_bp, url_prefix="/requests")

    return app
