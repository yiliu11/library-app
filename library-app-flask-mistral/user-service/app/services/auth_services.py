from flask import current_app
from werkzeug.exceptions import Unauthorized, BadRequest, Conflict, NotFound
from app.repositories.user_repository import UserRepository
from app.utils.security import SecurityManager
from app.utils.validators import Validators
from app.models.user import UserRole

class AuthService:
    @staticmethod
    def login(username, password):
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise Unauthorized('Invalid username or password')

        if not user.is_active:
            raise Unauthorized('Account is locked. Please contact support.')

        if not user.check_password(password, current_app.bcrypt):
            user.increment_failed_attempts()
            UserRepository.update_user(user)
            raise Unauthorized('Invalid username or password')

        user.reset_failed_attempts()
        user.last_login = datetime.utcnow()
        UserRepository.update_user(user)

        token = SecurityManager.generate_jwt_token(user.id, user.role.value)
        return {'token': token, 'role': user.role.value}

    @staticmethod
    def register_user(username, email, role, requesting_user_role):
        if requesting_user_role != UserRole.LIBRARIAN.value:
            raise Unauthorized('Only librarians can register new users')

        Validators.validate_username(username)
        Validators.validate_email(email)
        Validators.validate_role(role)

        password = SecurityManager.generate_password_reset_token(email)[:12]  # Generate a temporary password
        password_hash = SecurityManager.generate_password_hash(password)

        user = UserRepository.create_user(username, email, password_hash, role)

        # In a real app, you would send the password to the user's email
        current_app.logger.info(f'New user registered: {username}. Temporary password: {password}')

        return user.to_dict()

    @staticmethod
    def request_password_reset(email):
        user = UserRepository.get_user_by_email(email)
        if not user:
            raise NotFound('User not found')

        token = SecurityManager.generate_password_reset_token(email)
        # In a real app, you would send an email with a reset link containing the token
        current_app.logger.info(f'Password reset requested for: {email}. Token: {token}')

        return {'message': 'Password reset link sent to your email'}
