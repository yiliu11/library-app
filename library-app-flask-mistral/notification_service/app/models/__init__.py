# Import models to make them available at the package level
from .notification import Notification, NotificationType, NotificationStatus

# Expose the models
__all__ = ['Notification', 'NotificationType', 'NotificationStatus']
