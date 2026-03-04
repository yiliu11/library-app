from flask import request, jsonify
from flask_restx import Namespace, Resource
from app.dtos.auth_dto import LoginRequestDTO, LoginResponseDTO, UserRegistrationDTO, PasswordResetRequestDTO
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('auth', description='Authentication operations')

@api.route('/login')
class Login(Resource):
    @api.expect(LoginRequestDTO.api_model)
    def post(self):
        """User login"""
        data = request.get_json()
        try:
            result = AuthService.login(data['username'], data['password'])
            return LoginResponseDTO.api_model(result), 200
        except Exception as e:
            return {'error': str(e)}, 401

@api.route('/register')
class Register(Resource):
    @api.expect(UserRegistrationDTO.api_model)
    @jwt_required()
    def post(self):
        """Register a new user (librarian only)"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            user = AuthService.register_user(
                data['username'],
                data['email'],
                data['role'],
                current_user['role']
            )
            return user, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/password-reset')
class PasswordReset(Resource):
    @api.expect(PasswordResetRequestDTO.api_model)
    def post(self):
        """Request password reset"""
        data = request.get_json()
        try:
            result = AuthService.request_password_reset(data['email'])
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 400
