import re
from werkzeug.exceptions import BadRequest

class RequestValidators:
    @staticmethod
    def validate_book_title(title):
        if not title or len(title) < 2 or len(title) > 255:
            raise BadRequest('Title must be between 2 and 255 characters')

    @staticmethod
    def validate_book_author(author):
        if not author or len(author) < 2 or len(author) > 100:
            raise BadRequest('Author must be between 2 and 100 characters')

    @staticmethod
    def validate_isbn(isbn):
        if isbn and (len(isbn) < 10 or len(isbn) > 20):
            raise BadRequest('ISBN must be between 10 and 20 characters')
        if isbn and not re.match(r'^\d{10,20}$', isbn.replace('-', '')):
            raise BadRequest('Invalid ISBN format')

    @staticmethod
    def validate_request_status(status):
        valid_statuses = ['PENDING', 'APPROVED', 'REJECTED', 'ARCHIVED']
        if status and status not in valid_statuses:
            raise BadRequest(f'Invalid request status. Must be one of: {", ".join(valid_statuses)}')

    @staticmethod
    def validate_notes(notes, max_length=500):
        if notes and len(notes) > max_length:
            raise BadRequest(f'Notes must be less than {max_length} characters')
