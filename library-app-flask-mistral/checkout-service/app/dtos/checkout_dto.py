from flask_restx import fields
from enum import Enum

class CheckoutStatusEnum(Enum):
    ACTIVE = 'ACTIVE'
    OVERDUE = 'OVERDUE'
    RETURNED = 'RETURNED'
    RENEWED = 'RENEWED'

class CheckoutRequestDTO:
    api_model = {
        'user_id': fields.Integer(required=True, description='User ID'),
        'book_id': fields.Integer(required=True, description='Book ID')
    }

class CheckoutResponseDTO:
    api_model = {
        'id': fields.Integer(required=True, description='Checkout ID'),
        'user_id': fields.Integer(required=True, description='User ID'),
        'book_id': fields.Integer(required=True, description='Book ID'),
        'checkout_date': fields.DateTime(required=True, description='Checkout date'),
        'due_date': fields.DateTime(required=True, description='Due date'),
        'return_date': fields.DateTime(description='Return date'),
        'status': fields.String(required=True, description='Checkout status',
                                enum=CheckoutStatusEnum._member_names_),
        'fine_amount': fields.Float(required=True, description='Fine amount'),
        'created_at': fields.DateTime(required=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(required=True, description='Last update timestamp')
    }

class RenewalRequestDTO:
    api_model = {
        'checkout_id': fields.Integer(required=True, description='Checkout ID')
    }

class ReturnRequestDTO:
    api_model = {
        'checkout_id': fields.Integer(required=True, description='Checkout ID')
    }

class UserRecordDTO:
    api_model = {
        'user_id': fields.Integer(required=True, description='User ID'),
        'checked_out_items': fields.List(fields.Nested({
            'checkout_id': fields.Integer(required=True, description='Checkout ID'),
            'book_id': fields.Integer(required=True, description='Book ID'),
            'book_title': fields.String(required=True, description='Book title'),
            'due_date': fields.DateTime(required=True, description='Due date'),
            'status': fields.String(required=True, description='Checkout status',
                                   enum=CheckoutStatusEnum._member_names_),
            'fine_amount': fields.Float(required=True, description='Fine amount')
        })),
        'total_fines': fields.Float(required=True, description='Total fines')
    }
