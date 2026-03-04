from flask import Blueprint
from flask_restx import Api
from app.controllers.checkout_controller import api as checkout_ns

checkout_bp = Blueprint('checkout', __name__)
api = Api(checkout_bp, version='1.0', title='Checkout Service API', description='Book checkout and management')

api.add_namespace(checkout_ns, path='/checkout')
