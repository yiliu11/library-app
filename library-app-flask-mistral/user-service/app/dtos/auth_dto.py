from flask_restx import Namespace, fields
from enum import Enum

class UserRoleEnum(Enum):
    PATRON = 'PATRON'
    STAFF = 'STAFF'
    LIBRARIAN = 'LIBRARIAN'

class LoginRequestDTO:
    api_model = {
        'username': fields.String(required=True, description='User username'),
        'password': fields.String(required=True, description='User password')
    }

class LoginResponseDTO:
    api_model = {
        'token': fields.String(required=True, description='JWT access token'),
        'role': fields.String(required=True, description='User role', enum=UserRoleEnum._member_names_)
    }

class UserRegistrationDTO:
    api_model = {
        'username': fields.String(required=True, description='User username'),
        'email': fields.String(required=True, description='User email'),
        'role': fields.String(required=True, description='User role', enum=UserRoleEnum._member_names_)
    }

class PasswordResetRequestDTO:
    api_model = {
        'email': fields.String(required=True, description='User email')
    }
