import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    SECRET_KEY = os.getenv("SECRET_KEY") or "replace_this"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET = os.getenv("JWT_SECRET") or "replace-me"
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS") or 3600)

    # Login attempt policy
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS") or 5)
    LOCKOUT_SECONDS = int(os.getenv("LOCKOUT_SECONDS") or 900)

    # Other
    REQUESTS_TIMEOUT = 5  # seconds for inter-service REST calls
