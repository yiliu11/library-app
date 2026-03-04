import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

    # Database config
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/library_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API config
    CHECKOUT_SERVICE_API_KEY = os.getenv('CHECKOUT_SERVICE_API_KEY', 'default-checkout-service-key')

    # Checkout config
    MAX_CHECKOUT_DAYS = int(os.getenv('MAX_CHECKOUT_DAYS', 14))
    MAX_CHECKOUTS_PER_USER = int(os.getenv('MAX_CHECKOUTS_PER_USER', 5))
    RENEWAL_DAYS = int(os.getenv('RENEWAL_DAYS', 7))
    DAILY_FINE_AMOUNT = float(os.getenv('DAILY_FINE_AMOUNT', 0.50))

    # Logging config
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # External service URLs
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5000/api')
    BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://localhost:5001/api')
