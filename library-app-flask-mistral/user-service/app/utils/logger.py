import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/user_service.log',
        maxBytes=1024 * 1024 * 10,  # 10 MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(app.config['LOG_LEVEL'])

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(app.config['LOG_LEVEL'])

    # Remove default handlers and add our handlers
    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.info('User Service started')
