from flask import Blueprint
from flask_restx import Api
from app.controllers.auth_controller import api as auth_ns

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp, version='1.0', title='User Service API', description='User authentication and management')

api.add_namespace(auth_ns, path='/auth')
