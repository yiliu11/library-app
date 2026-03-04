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
    NOTIFICATION_SERVICE_API_KEY = os.getenv('NOTIFICATION_SERVICE_API_KEY', 'default-notification-service-key')

    # Email config
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'notifications@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'email-password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'notifications@example.com')

    # SMS config
    SMS_PROVIDER = os.getenv('SMS_PROVIDER', 'twilio')
    SMS_ACCOUNT_SID = os.getenv('SMS_ACCOUNT_SID', 'your-account-sid')
    SMS_AUTH_TOKEN = os.getenv('SMS_AUTH_TOKEN', 'your-auth-token')
    SMS_FROM_NUMBER = os.getenv('SMS_FROM_NUMBER', '+1234567890')

    # Notification config
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY_SECONDS = int(os.getenv('RETRY_DELAY_SECONDS', 60))

    # Logging config
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
