from werkzeug.exceptions import BadRequest
from datetime import datetime

class CheckoutValidators:
    @staticmethod
    def validate_user_id(user_id):
        if not user_id or user_id <= 0:
            raise BadRequest('Invalid user ID')

    @staticmethod
    def validate_book_id(book_id):
        if not book_id or book_id <= 0:
            raise BadRequest('Invalid book ID')

    @staticmethod
    def validate_checkout_id(checkout_id):
        if not checkout_id or checkout_id <= 0:
            raise BadRequest('Invalid checkout ID')

    @staticmethod
    def validate_checkout_status(status):
        valid_statuses = ['ACTIVE', 'OVERDUE', 'RETURNED', 'RENEWED']
        if status and status not in valid_statuses:
            raise BadRequest(f'Invalid checkout status. Must be one of: {", ".join(valid_statuses)}')

    @staticmethod
    def validate_date(date_str, date_format='%Y-%m-%d'):
        try:
            datetime.strptime(date_str, date_format)
        except ValueError:
            raise BadRequest('Invalid date format. Use YYYY-MM-DD')
