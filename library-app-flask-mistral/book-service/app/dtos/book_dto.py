from flask_restx import fields
from enum import Enum

class AvailabilityStatusEnum(Enum):
    AVAILABLE = 'AVAILABLE'
    CHECKED_OUT = 'CHECKED_OUT'
    RESERVED = 'RESERVED'
    LOST = 'LOST'

class BookRequestDTO:
    api_model = {
        'title': fields.String(required=True, description='Book title'),
        'author': fields.String(required=True, description='Book author'),
        'isbn': fields.String(required=True, description='Book ISBN'),
        'publication_date': fields.Date(description='Publication date')
    }

class BookResponseDTO:
    api_model = {
        'id': fields.Integer(required=True, description='Book ID'),
        'title': fields.String(required=True, description='Book title'),
        'author': fields.String(required=True, description='Book author'),
        'isbn': fields.String(required=True, description='Book ISBN'),
        'publication_date': fields.Date(description='Publication date'),
        'availability_status': fields.String(required=True, description='Availability status',
                                             enum=AvailabilityStatusEnum._member_names_),
        'created_at': fields.DateTime(required=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(required=True, description='Last update timestamp')
    }

class BookSearchDTO:
    api_model = {
        'search_term': fields.String(required=True, description='Search term'),
        'search_by': fields.String(required=True, description='Search by field (title/author/isbn)',
                                    enum=['title', 'author', 'isbn'])
    }

class BookUpdateDTO:
    api_model = {
        'title': fields.String(description='Book title'),
        'author': fields.String(description='Book author'),
        'isbn': fields.String(description='Book ISBN'),
        'publication_date': fields.Date(description='Publication date'),
        'availability_status': fields.String(description='Availability status',
                                              enum=AvailabilityStatusEnum._member_names_)
    }
