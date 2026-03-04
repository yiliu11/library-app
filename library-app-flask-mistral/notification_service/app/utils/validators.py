import re
from werkzeug.exceptions import BadRequest

class NotificationValidators:
    @staticmethod
    def validate_email(email):
        if not email or len(email) > 100:
            raise BadRequest('Email must be provided and less than 100 characters')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise BadRequest('Invalid email format')

    @staticmethod
    def validate_phone(phone):
        if phone and not re.match(r'^\+?[0-9\s\-\(\)]{7,20}$', phone):
            raise BadRequest('Invalid phone number format')

    @staticmethod
    def validate_notification_type(notification_type):
        valid_types = [
            'OVERDUE_BOOK', 'REQUEST_APPROVED', 'REQUEST_REJECTED',
            'DUE_DATE_REMINDER', 'PASSWORD_RESET', 'CHECKOUT_CONFIRMATION',
            'RENEWAL_CONFIRMATION', 'REQUEST_SUBMITTED'
        ]
        if notification_type not in valid_types:
            raise BadRequest(f'Invalid notification type. Must be one of: {", ".join(valid_types)}')

    @staticmethod
    def validate_recipient(recipient_email=None, recipient_phone=None):
        if not recipient_email and not recipient_phone:
            raise BadRequest('Either recipient_email or recipient_phone must be provided')
