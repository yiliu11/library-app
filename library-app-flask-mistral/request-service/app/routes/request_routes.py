from flask import Blueprint
from flask_restx import Api
from app.controllers.request_controller import api as request_ns

request_bp = Blueprint('request', __name__)
api = Api(request_bp, version='1.0', title='Request Service API', description='Book request management')

api.add_namespace(request_ns, path='/requests')
