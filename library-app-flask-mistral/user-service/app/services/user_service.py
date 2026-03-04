from flask import current_app
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound
from app.repositories.user_repository import UserRepository
from app.utils.security import SecurityManager
from app.utils.validators import Validators
from app.models.user import UserRole

class UserService:
    @staticmethod
    def get_user_by_id(user_id, requesting_user_id, requesting_user_role):
        user = UserRepository.get_user_by_id(user_id)

        # Only allow access if:
        # 1. The user is requesting their own data, OR
        # 2. The requesting user is a librarian
        if user.id != requesting_user_id and requesting_user_role != UserRole.LIBRARIAN.value:
            raise Unauthorized('You are not authorized to access this resource')

        return user.to_dict()

    @staticmethod
    def get_all_users(requesting_user_role):
        if requesting_user_role != UserRole.LIBRARIAN.value:
            raise Unauthorized('Only librarians can access all user records')

        users = UserRepository.get_all_users()
        return [user.to_dict() for user in users]

    @staticmethod
    def update_user(user_id, update_data, requesting_user_id, requesting_user_role):
        # Check if the requesting user has permission
        if user_id != requesting_user_id and requesting_user_role != UserRole.LIBRARIAN.value:
            raise Unauthorized('You are not authorized to update this user')

        user = UserRepository.get_user_by_id(user_id)

        # Validate and update fields
        if 'email' in update_data:
            Validators.validate_email(update_data['email'])
            user.email = update_data['email']

        if 'password' in update_data:
            Validators.validate_password(update_data['password'])
            user.password_hash = SecurityManager.generate_password_hash(update_data['password'])

        if 'is_active' in update_data and requesting_user_role == UserRole.LIBRARIAN.value:
            user.is_active = update_data['is_active']

        updated_user = UserRepository.update_user(user)
        return updated_user.to_dict()
