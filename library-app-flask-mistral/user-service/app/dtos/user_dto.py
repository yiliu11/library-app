from flask_restx import fields

class UserDTO:
    api_model = {
        'id': fields.Integer(required=True, description='User ID'),
        'username': fields.String(required=True, description='User username'),
        'email': fields.String(required=True, description='User email'),
        'role': fields.String(required=True, description='User role'),
        'is_active': fields.Boolean(required=True, description='Is user active'),
        'created_at': fields.DateTime(required=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(required=True, description='Last update timestamp')
    }
