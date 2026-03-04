from flask_restx import fields
from enum import Enum

class NotificationTypeEnum(Enum):
    OVERDUE_BOOK = 'OVERDUE_BOOK'
    REQUEST_APPROVED = 'REQUEST_APPROVED'
    REQUEST_REJECTED = 'REQUEST_REJECTED'
    DUE_DATE_REMINDER = 'DUE_DATE_REMINDER'
    PASSWORD_RESET = 'PASSWORD_RESET'
    CHECKOUT_CONFIRMATION = 'CHECKOUT_CONFIRMATION'
    RENEWAL_CONFIRMATION = 'RENEWAL_CONFIRMATION'
    REQUEST_SUBMITTED = 'REQUEST_SUBMITTED'

class NotificationStatusEnum(Enum):
    PENDING = 'PENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'

class EmailNotificationDTO:
    api_model = {
        'to': fields.String(required=True, description='Recipient email'),
        'subject': fields.String(required=True, description='Email subject'),
        'body': fields.String(required=True, description='Email body')
    }

class SMSNotificationDTO:
    api_model = {
        'to': fields.String(required=True, description='Recipient phone number'),
        'message': fields.String(required=True, description='SMS message')
    }

class NotificationRequestDTO:
    api_model = {
        'recipient_id': fields.Integer(description='Recipient user ID'),
        'recipient_email': fields.String(description='Recipient email'),
        'recipient_phone': fields.String(description='Recipient phone number'),
        'subject': fields.String(required=True, description='Notification subject'),
        'message': fields.String(required=True, description='Notification message'),
        'notification_type': fields.String(required=True, description='Notification type',
                                           enum=NotificationTypeEnum._member_names_),
        'metadata': fields.Raw(description='Additional metadata')
    }

class NotificationResponseDTO:
    api_model = {
        'id': fields.Integer(required=True, description='Notification ID'),
        'recipient_id': fields.Integer(description='Recipient user ID'),
        'recipient_email': fields.String(description='Recipient email'),
        'recipient_phone': fields.String(description='Recipient phone number'),
        'subject': fields.String(required=True, description='Notification subject'),
        'message': fields.String(required=True, description='Notification message'),
        'notification_type': fields.String(required=True, description='Notification type',
                                           enum=NotificationTypeEnum._member_names_),
        'status': fields.String(required=True, description='Notification status',
                                enum=NotificationStatusEnum._member_names_),
        'created_at': fields.DateTime(required=True, description='Creation timestamp'),
        'sent_at': fields.DateTime(description='Sent timestamp'),
        'retry_count': fields.Integer(description='Number of retry attempts'),
        'metadata': fields.Raw(description='Additional metadata'),
        'error_message': fields.String(description='Error message if failed')
    }

class RoleNotificationDTO:
    api_model = {
        'recipient_role': fields.String(required=True, description='Recipient role (e.g., LIBRARIAN)'),
        'subject': fields.String(required=True, description='Notification subject'),
        'message': fields.String(required=True, description='Notification message'),
        'notification_type': fields.String(required=True, description='Notification type',
                                           enum=NotificationTypeEnum._member_names_),
        'metadata': fields.Raw(description='Additional metadata')
    }
