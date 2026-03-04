# Import DTOs to make them available at the package level
from .notification_dto import (
    NotificationRequestDTO, NotificationResponseDTO,
    EmailNotificationDTO, SMSNotificationDTO, RoleNotificationDTO
)

# Expose the DTOs
__all__ = [
    'NotificationRequestDTO', 'NotificationResponseDTO',
    'EmailNotificationDTO', 'SMSNotificationDTO', 'RoleNotificationDTO'
]
