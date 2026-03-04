from app import db
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    OVERDUE_BOOK = 'OVERDUE_BOOK'
    REQUEST_APPROVED = 'REQUEST_APPROVED'
    REQUEST_REJECTED = 'REQUEST_REJECTED'
    DUE_DATE_REMINDER = 'DUE_DATE_REMINDER'
    PASSWORD_RESET = 'PASSWORD_RESET'
    CHECKOUT_CONFIRMATION = 'CHECKOUT_CONFIRMATION'
    RENEWAL_CONFIRMATION = 'RENEWAL_CONFIRMATION'
    REQUEST_SUBMITTED = 'REQUEST_SUBMITTED'

class NotificationStatus(Enum):
    PENDING = 'PENDING'
    SENT = 'SENT'
    FAILED = 'FAILED'

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.BigInteger)
    recipient_email = db.Column(db.String(100))
    recipient_phone = db.Column(db.String(20))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text)
    notification_type = db.Column(db.Enum(NotificationType), nullable=False)
    status = db.Column(db.Enum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sent_at = db.Column(db.DateTime)
    retry_count = db.Column(db.Integer, default=0)
    metadata = db.Column(db.JSON)
    error_message = db.Column(db.Text)

    def __repr__(self):
        return f'<Notification {self.id} to {self.recipient_email or self.recipient_phone}>'

    def to_dict(self):
        return {
            'id': self.id,
            'recipient_id': self.recipient_id,
            'recipient_email': self.recipient_email,
            'recipient_phone': self.recipient_phone,
            'subject': self.subject,
            'message': self.message,
            'notification_type': self.notification_type.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'retry_count': self.retry_count,
            'metadata': self.metadata,
            'error_message': self.error_message
        }

    def mark_as_sent(self):
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.utcnow()

    def mark_as_failed(self, error_message):
        self.status = NotificationStatus.FAILED
        self.error_message = error_message
        self.retry_count += 1
