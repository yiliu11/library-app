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
    BOOK_SERVICE_API_KEY = os.getenv('BOOK_SERVICE_API_KEY', 'default-book-service-key')

    # Security config
    MAX_BOOK_SEARCH_RESULTS = int(os.getenv('MAX_BOOK_SEARCH_RESULTS', 100))
    RATE_LIMIT_SEARCH = int(os.getenv('RATE_LIMIT_SEARCH', 100))  # requests per minute

    # Logging config
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
