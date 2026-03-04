from app import db
from app.models.notification import Notification, NotificationStatus
from werkzeug.exceptions import NotFound

class NotificationRepository:
    @staticmethod
    def save_notification(notification):
        db.session.add(notification)
        db.session.commit()
        return notification

    @staticmethod
    def get_notification_by_id(notification_id):
        notification = Notification.query.get(notification_id)
        if not notification:
            raise NotFound('Notification not found')
        return notification

    @staticmethod
    def update_notification(notification):
        db.session.commit()
        return notification

    @staticmethod
    def get_failed_notifications(max_retries=3):
        return Notification.query.filter(
            Notification.status == NotificationStatus.FAILED,
            Notification.retry_count < max_retries
        ).all()

    @staticmethod
    def get_notifications_by_recipient(recipient_id=None, recipient_email=None, recipient_phone=None):
        query = Notification.query

        if recipient_id:
            query = query.filter_by(recipient_id=recipient_id)
        if recipient_email:
            query = query.filter_by(recipient_email=recipient_email)
        if recipient_phone:
            query = query.filter_by(recipient_phone=recipient_phone)

        return query.all()

    @staticmethod
    def get_pending_notifications(limit=100):
        return Notification.query.filter_by(
            status=NotificationStatus.PENDING
        ).order_by(Notification.created_at).limit(limit).all()
