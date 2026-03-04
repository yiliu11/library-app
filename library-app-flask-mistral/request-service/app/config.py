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
    REQUEST_SERVICE_API_KEY = os.getenv('REQUEST_SERVICE_API_KEY', 'default-request-service-key')

    # External service URLs
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5000/api')
    BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://localhost:5001/api')
    NOTIFICATION_SERVICE_URL = os.getenv('NOTIFICATION_SERVICE_URL', 'http://localhost:5004/api')

    # Request config
    MAX_REQUEST_NOTES_LENGTH = int(os.getenv('MAX_REQUEST_NOTES_LENGTH', 500))

    # Logging config
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
