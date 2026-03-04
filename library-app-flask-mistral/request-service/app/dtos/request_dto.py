from flask_restx import fields
from enum import Enum

class RequestStatusEnum(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    ARCHIVED = 'ARCHIVED'

class BookRequestDTO:
    api_model = {
        'book_title': fields.String(required=True, description='Book title'),
        'book_author': fields.String(required=True, description='Book author'),
        'book_isbn': fields.String(description='Book ISBN')
    }

class BookRequestResponseDTO:
    api_model = {
        'id': fields.Integer(required=True, description='Request ID'),
        'book_title': fields.String(required=True, description='Book title'),
        'book_author': fields.String(required=True, description='Book author'),
        'book_isbn': fields.String(description='Book ISBN'),
        'requester_id': fields.Integer(required=True, description='Requester ID'),
        'request_date': fields.DateTime(required=True, description='Request date'),
        'status': fields.String(required=True, description='Request status',
                                enum=RequestStatusEnum._member_names_),
        'decision_date': fields.DateTime(description='Decision date'),
        'decided_by': fields.Integer(description='Decided by user ID'),
        'notes': fields.String(description='Decision notes')
    }

class RequestDecisionDTO:
    api_model = {
        'request_id': fields.Integer(required=True, description='Request ID'),
        'status': fields.String(required=True, description='Decision status',
                               enum=['APPROVED', 'REJECTED']),
        'notes': fields.String(description='Decision notes')
    }

class RequestSearchDTO:
    api_model = {
        'status': fields.String(description='Request status to filter by',
                                enum=['PENDING', 'APPROVED', 'REJECTED', 'ARCHIVED'])
    }
