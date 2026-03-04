import re
from werkzeug.exceptions import BadRequest

class BookValidators:
    @staticmethod
    def validate_title(title):
        if not title or len(title) < 2 or len(title) > 255:
            raise BadRequest('Title must be between 2 and 255 characters')

    @staticmethod
    def validate_author(author):
        if not author or len(author) < 2 or len(author) > 100:
            raise BadRequest('Author must be between 2 and 100 characters')

    @staticmethod
    def validate_isbn(isbn):
        if not isbn or len(isbn) < 10 or len(isbn) > 20:
            raise BadRequest('ISBN must be between 10 and 20 characters')
        # Basic ISBN validation (can be enhanced)
        if not re.match(r'^\d{10,20}$', isbn.replace('-', '')):
            raise BadRequest('Invalid ISBN format')

    @staticmethod
    def validate_availability_status(status):
        valid_statuses = ['AVAILABLE', 'CHECKED_OUT', 'RESERVED', 'LOST']
        if status and status not in valid_statuses:
            raise BadRequest(f'Invalid availability status. Must be one of: {", ".join(valid_statuses)}')

    @staticmethod
    def validate_search_criteria(criteria):
        valid_criteria = ['title', 'author', 'isbn']
        if criteria not in valid_criteria:
            raise BadRequest(f'Invalid search criteria. Must be one of: {", ".join(valid_criteria)}')
