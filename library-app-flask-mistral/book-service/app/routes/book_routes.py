from flask import Blueprint
from flask_restx import Api
from app.controllers.book_controller import api as book_ns

book_bp = Blueprint('book', __name__)
api = Api(book_bp, version='1.0', title='Book Service API', description='Book inventory and management')

api.add_namespace(book_ns, path='/books')
