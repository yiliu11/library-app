import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    SECRET_KEY = os.getenv("SECRET_KEY") or "replace_me"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///dev_checkout.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET") or "replace_me"
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"

    # clients
    REQUESTS_TIMEOUT = int(os.getenv("REQUESTS_TIMEOUT") or 5)
    CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL") or "http://localhost:5001"

    # Loan policy
    MAX_RENEWALS = int(os.getenv("MAX_RENEWALS") or 2)
    LOAN_PERIOD_DAYS = int(os.getenv("LOAN_PERIOD_DAYS") or 14)
