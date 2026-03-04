import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

    SECRET_KEY = os.getenv("SECRET_KEY") or "replace_me"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///dev_user_mgmt.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT validation (must match Authentication Service)
    JWT_SECRET = os.getenv("JWT_SECRET") or "replace_me"
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"

    # Inter-service REST
    REQUESTS_TIMEOUT = int(os.getenv("REQUESTS_TIMEOUT") or 5)
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL") or "http://localhost:5000"

    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE") or 20)
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE") or 100)
