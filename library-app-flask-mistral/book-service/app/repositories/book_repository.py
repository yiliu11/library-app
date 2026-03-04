from app import db
from app.models.book import Book, AvailabilityStatus
from werkzeug.exceptions import NotFound, Conflict
from sqlalchemy.exc import SQLAlchemyError
from app.utils.validators import BookValidators

class BookRepository:
    @staticmethod
    def get_book_by_id(book_id):
        book = Book.query.get(book_id)
        if not book:
            raise NotFound('Book not found')
        return book

    @staticmethod
    def get_book_by_isbn(isbn):
        BookValidators.validate_isbn(isbn)
        book = Book.query.filter_by(isbn=isbn).first()
        if not book:
            raise NotFound('Book not found')
        return book

    @staticmethod
    def create_book(title, author, isbn, publication_date=None):
        BookValidators.validate_title(title)
        BookValidators.validate_author(author)
        BookValidators.validate_isbn(isbn)

        if Book.query.filter_by(isbn=isbn).first():
            raise Conflict('Book with this ISBN already exists')

        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publication_date=publication_date
        )
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def update_book(book_id, update_data):
        book = BookRepository.get_book_by_id(book_id)

        if 'title' in update_data:
            BookValidators.validate_title(update_data['title'])
            book.title = update_data['title']

        if 'author' in update_data:
            BookValidators.validate_author(update_data['author'])
            book.author = update_data['author']

        if 'isbn' in update_data:
            BookValidators.validate_isbn(update_data['isbn'])
            if update_data['isbn'] != book.isbn and Book.query.filter_by(isbn=update_data['isbn']).first():
                raise Conflict('Book with this ISBN already exists')
            book.isbn = update_data['isbn']

        if 'publication_date' in update_data:
            book.publication_date = update_data['publication_date']

        if 'availability_status' in update_data:
            BookValidators.validate_availability_status(update_data['availability_status'])
            book.update_availability(update_data['availability_status'])

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = BookRepository.get_book_by_id(book_id)
        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def search_books(search_term, search_by, limit=100):
        BookValidators.validate_search_criteria(search_by)

        if search_by == 'title':
            return Book.query.filter(Book.title.ilike(f'%{search_term}%')).limit(limit).all()
        elif search_by == 'author':
            return Book.query.filter(Book.author.ilike(f'%{search_term}%')).limit(limit).all()
        elif search_by == 'isbn':
            return Book.query.filter(Book.isbn.ilike(f'%{search_term}%')).limit(limit).all()

    @staticmethod
    def get_all_books(limit=100):
        return Book.query.limit(limit).all()
