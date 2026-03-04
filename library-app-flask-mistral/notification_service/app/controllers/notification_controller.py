from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dtos.notification_dto import (
    NotificationRequestDTO, NotificationResponseDTO,
    EmailNotificationDTO, SMSNotificationDTO, RoleNotificationDTO
)
from app.services.notification_service import NotificationService
from app.utils.validators import NotificationValidators

api = Namespace('notifications', description='Notification operations')

@api.route('/')
class NotificationList(Resource):
    @api.expect(NotificationRequestDTO.api_model)
    @jwt_required()
    def post(self):
        """Create and send a notification"""
        data = request.get_json()
        try:
            notification = NotificationService.create_notification(
                recipient_id=data.get('recipient_id'),
                recipient_email=data.get('recipient_email'),
                recipient_phone=data.get('recipient_phone'),
                subject=data['subject'],
                message=data['message'],
                notification_type=data['notification_type'],
                metadata=data.get('metadata')
            )

            success = NotificationService.send_notification(notification.id)
            if not success:
                return {'message': 'Notification created but sending failed', 'notification_id': notification.id}, 202

            return NotificationResponseDTO.api_model(notification), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<int:notification_id>')
@api.param('notification_id', 'Notification ID')
class NotificationDetail(Resource):
    @api.marshal_with(NotificationResponseDTO.api_model)
    @jwt_required()
    def get(self, notification_id):
        """Get notification status"""
        try:
            notification = NotificationService.get_notification_status(notification_id)
            return notification, 200
        except Exception as e:
            return {'error': str(e)}, 404

@api.route('/email')
class EmailNotification(Resource):
    @api.expect(EmailNotificationDTO.api_model)
    @jwt_required()
    def post(self):
        """Send an email notification"""
        data = request.get_json()
        try:
            NotificationValidators.validate_email(data['to'])

            success = NotificationService.send_email_notification(
                data['to'],
                data['subject'],
                data['body'],
                'GENERAL_NOTIFICATION',  # Default type
                {'delivery_method': 'email'}
            )

            if success:
                return {'message': 'Email sent successfully'}, 200
            else:
                return {'message': 'Email sending failed'}, 500
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/sms')
class SMSNotification(Resource):
    @api.expect(SMSNotificationDTO.api_model)
    @jwt_required()
    def post(self):
        """Send an SMS notification"""
        data = request.get_json()
        try:
            NotificationValidators.validate_phone(data['to'])

            success = NotificationService.send_sms_notification(
                data['to'],
                data['message'],
                'GENERAL_NOTIFICATION',  # Default type
                {'delivery_method': 'sms'}
            )

            if success:
                return {'message': 'SMS sent successfully'}, 200
            else:
                return {'message': 'SMS sending failed'}, 500
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/role')
class RoleNotification(Resource):
    @api.expect(RoleNotificationDTO.api_model)
    @jwt_required()
    def post(self):
        """Send a notification to all users with a specific role"""
        data = request.get_json()
        try:
            success = NotificationService.send_role_notification(
                data['recipient_role'],
                data['subject'],
                data['message'],
                data['notification_type'],
                data.get('metadata')
            )

            if success:
                return {'message': f'Notification sent to all {data["recipient_role"]}s'}, 200
            else:
                return {'message': 'Notification sending failed'}, 500
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/retry')
class RetryNotifications(Resource):
    @jwt_required()
    def post(self):
        """Retry sending failed notifications"""
        try:
            result = NotificationService.retry_failed_notifications()
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 500
