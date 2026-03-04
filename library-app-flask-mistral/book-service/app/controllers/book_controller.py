from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dtos.book_dto import BookRequestDTO, BookResponseDTO, BookSearchDTO, BookUpdateDTO
from app.services.book_service import BookService
from app.utils.logger import setup_logging

api = Namespace('books', description='Book operations')

@api.route('/')
class BookList(Resource):
    @api.expect(BookRequestDTO.api_model)
    @jwt_required()
    def post(self):
        """Add a new book (librarian only)"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            book = BookService.create_book(
                data['title'],
                data['author'],
                data['isbn'],
                data.get('publication_date'),
                current_user['role']
            )
            return BookResponseDTO.api_model(book), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(BookResponseDTO.api_model)
    @jwt_required(optional=True)  # Public read access
    def get(self):
        """Get all books"""
        try:
            current_user = get_jwt_identity() if 'Authorization' in request.headers else None
            user_role = current_user['role'] if current_user else None
            books = BookService.get_all_books(user_role)
            return books, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<int:book_id>')
@api.param('book_id', 'Book ID')
class Book(Resource):
    @api.marshal_with(BookResponseDTO.api_model)
    @jwt_required(optional=True)  # Public read access
    def get(self, book_id):
        """Get book details"""
        try:
            book = BookService.get_book_by_id(book_id)
            return book, 200
        except Exception as e:
            return {'error': str(e)}, 404

    @api.expect(BookUpdateDTO.api_model)
    @jwt_required()
    def put(self, book_id):
        """Update book details (librarian only)"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            book = BookService.update_book(book_id, data, current_user['role'])
            return BookResponseDTO.api_model(book), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, book_id):
        """Delete a book (librarian only)"""
        current_user = get_jwt_identity()
        try:
            result = BookService.delete_book(book_id, current_user['role'])
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/search')
class BookSearch(Resource):
    @api.expect(BookSearchDTO.api_model)
    @api.marshal_list_with(BookResponseDTO.api_model)
    @jwt_required(optional=True)  # Public read access
    @api.doc(security=[])  # Optional auth
    def post(self):
        """Search for books"""
        data = request.get_json()
        try:
            current_user = get_jwt_identity() if 'Authorization' in request.headers else None
            user_role = current_user['role'] if current_user else None
            books = BookService.search_books(data['search_term'], data['search_by'], user_role)
            return books, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<int:book_id>/availability')
@api.param('book_id', 'Book ID')
class BookAvailability(Resource):
    @api.expect(api.model('AvailabilityUpdate', {
        'status': fields.String(required=True, description='New availability status',
                               enum=['AVAILABLE', 'CHECKED_OUT', 'RESERVED', 'LOST'])
    }))
    @jwt_required()
    def put(self, book_id):
        """Update book availability (librarian or checkout service only)"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            # For internal service-to-service communication, we might use an API key
            user_role = current_user['role'] if 'role' in current_user else 'CHECKOUT_SERVICE'
            book = BookService.update_book_availability(book_id, data['status'], user_role)
            return BookResponseDTO.api_model(book), 200
        except Exception as e:
            return {'error': str(e)}, 400
