from flask import current_app
from app.models.notification import Notification, NotificationStatus, NotificationType
from app.repositories.notification_repository import NotificationRepository
from app.services.email_service import EmailService
from app.services.sms_service import SMSService
from app.utils.validators import NotificationValidators
from werkzeug.exceptions import BadRequest, InternalServerError
import time
import threading

class NotificationService:
    @staticmethod
    def create_notification(recipient_id=None, recipient_email=None, recipient_phone=None,
                           subject=None, message=None, notification_type=None, metadata=None):
        NotificationValidators.validate_recipient(recipient_email, recipient_phone)
        NotificationValidators.validate_notification_type(notification_type)

        notification = Notification(
            recipient_id=recipient_id,
            recipient_email=recipient_email,
            recipient_phone=recipient_phone,
            subject=subject,
            message=message,
            notification_type=NotificationType[notification_type],
            metadata=metadata
        )

        NotificationRepository.save_notification(notification)
        return notification

    @staticmethod
    def send_notification(notification_id):
        notification = NotificationRepository.get_notification_by_id(notification_id)

        if notification.status != NotificationStatus.PENDING:
            raise BadRequest('Notification is not pending')

        success = False

        # Try to send email if recipient_email is provided
        if notification.recipient_email:
            success = EmailService.send_email(notification)

        # Try to send SMS if recipient_phone is provided and email failed or wasn't sent
        if not success and notification.recipient_phone:
            success = SMSService.send_sms(notification)

        if not success:
            # If both email and SMS fail, mark as failed
            if not notification.error_message:
                notification.mark_as_failed("Both email and SMS sending failed")
                NotificationRepository.update_notification(notification)

            # Schedule retry if max retries not reached
            if notification.retry_count < current_app.config['MAX_RETRIES']:
                current_app.logger.info(f"Scheduling retry for notification {notification.id}")
                NotificationService._schedule_retry(notification)

        return success

    @staticmethod
    def _schedule_retry(notification):
        delay = current_app.config['RETRY_DELAY_SECONDS'] * (notification.retry_count + 1)

        def retry_task():
            time.sleep(delay)
            try:
                current_app.logger.info(f"Retrying notification {notification.id}")
                NotificationService.send_notification(notification.id)
            except Exception as e:
                current_app.logger.error(f"Error in retry task: {str(e)}")

        thread = threading.Thread(target=retry_task)
        thread.daemon = True
        thread.start()

    @staticmethod
    def send_email_notification(to, subject, body, notification_type, metadata=None):
        notification = NotificationService.create_notification(
            recipient_email=to,
            subject=subject,
            message=body,
            notification_type=notification_type,
            metadata=metadata
        )

        return NotificationService.send_notification(notification.id)

    @staticmethod
    def send_sms_notification(to, message, notification_type, metadata=None):
        notification = NotificationService.create_notification(
            recipient_phone=to,
            subject="Library Notification",  # SMS doesn't use subject
            message=message,
            notification_type=notification_type,
            metadata=metadata
        )

        return NotificationService.send_notification(notification.id)

    @staticmethod
    def send_role_notification(recipient_role, subject, message, notification_type, metadata=None):
        # In a real application, you would query the user service for all users with this role
        # and send notifications to each of them
        # For this example, we'll just log the action

        current_app.logger.info(f"Would send notification to all {recipient_role}s: {subject}")

        # Create a notification record for auditing
        notification = NotificationService.create_notification(
            subject=subject,
            message=message,
            notification_type=notification_type,
            metadata={
                **metadata,
                'recipient_role': recipient_role
            }
        )

        # Mark as sent since we're not actually sending to individuals
        notification.mark_as_sent()
        NotificationRepository.update_notification(notification)

        return True

    @staticmethod
    def retry_failed_notifications():
        failed_notifications = NotificationRepository.get_failed_notifications(
            max_retries=current_app.config['MAX_RETRIES']
        )

        success_count = 0
        for notification in failed_notifications:
            try:
                if NotificationService.send_notification(notification.id):
                    success_count += 1
            except Exception as e:
                current_app.logger.error(f"Error retrying notification {notification.id}: {str(e)}")

        return {
            'message': f'Retried {len(failed_notifications)} failed notifications, {success_count} succeeded'
        }

    @staticmethod
    def get_notification_status(notification_id):
        notification = NotificationRepository.get_notification_by_id(notification_id)
        return notification.to_dict()
