from flask import current_app
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound, Conflict
from app.repositories.book_repository import BookRepository
from app.utils.validators import BookValidators
from app.models.book import AvailabilityStatus

class BookService:
    @staticmethod
    def get_book_by_id(book_id):
        return BookRepository.get_book_by_id(book_id).to_dict()

    @staticmethod
    def get_book_by_isbn(isbn):
        return BookRepository.get_book_by_isbn(isbn).to_dict()

    @staticmethod
    def create_book(title, author, isbn, publication_date=None, user_role=None):
        # Only librarians can add books
        if user_role != 'LIBRARIAN':
            raise Unauthorized('Only librarians can add books')

        book = BookRepository.create_book(title, author, isbn, publication_date)
        return book.to_dict()

    @staticmethod
    def update_book(book_id, update_data, user_role=None):
        # Only librarians can update books
        if user_role != 'LIBRARIAN':
            raise Unauthorized('Only librarians can update books')

        book = BookRepository.update_book(book_id, update_data)
        return book.to_dict()

    @staticmethod
    def delete_book(book_id, user_role=None):
        # Only librarians can delete books
        if user_role != 'LIBRARIAN':
            raise Unauthorized('Only librarians can delete books')

        BookRepository.delete_book(book_id)
        return {'message': 'Book deleted successfully'}

    @staticmethod
    def search_books(search_term, search_by, user_role=None):
        # Rate limiting is handled at the route level
        books = BookRepository.search_books(search_term, search_by, current_app.config['MAX_BOOK_SEARCH_RESULTS'])
        return [book.to_dict() for book in books]

    @staticmethod
    def get_all_books(user_role=None):
        books = BookRepository.get_all_books(current_app.config['MAX_BOOK_SEARCH_RESULTS'])
        return [book.to_dict() for book in books]

    @staticmethod
    def update_book_availability(book_id, new_status, user_role=None):
        # Only librarians or checkout service can update availability
        if user_role not in ['LIBRARIAN', 'CHECKOUT_SERVICE']:
            raise Unauthorized('Not authorized to update book availability')

        BookValidators.validate_availability_status(new_status)
        book = BookRepository.get_book_by_id(book_id)
        book.update_availability(new_status)
        BookRepository.update_book(book_id, {'availability_status': new_status})
        return book.to_dict()
