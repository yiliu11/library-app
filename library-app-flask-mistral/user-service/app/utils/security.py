from flask import current_app
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest

class SecurityManager:
    @staticmethod
    def generate_password_hash(password):
        return current_app.bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def generate_jwt_token(user_id, role):
        return create_access_token(identity={'user_id': user_id, 'role': role})

    @staticmethod
    def generate_password_reset_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt='password-reset-salt')

    @staticmethod
    def verify_password_reset_token(token, max_age=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
            return email
        except:
            raise BadRequest('Invalid or expired token')
