import re
from flask import current_app
from werkzeug.exceptions import BadRequest

class Validators:
    @staticmethod
    def validate_username(username):
        if not username or len(username) < 3 or len(username) > 50:
            raise BadRequest('Username must be between 3 and 50 characters')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise BadRequest('Username can only contain letters, numbers, and underscores')

    @staticmethod
    def validate_email(email):
        if not email or len(email) > 100:
            raise BadRequest('Email must be provided and less than 100 characters')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise BadRequest('Invalid email format')

    @staticmethod
    def validate_password(password):
        if not password or len(password) < 8:
            raise BadRequest('Password must be at least 8 characters long')

    @staticmethod
    def validate_role(role):
        valid_roles = ['PATRON', 'STAFF', 'LIBRARIAN']
        if role not in valid_roles:
            raise BadRequest(f'Invalid role. Must be one of: {", ".join(valid_roles)}')
