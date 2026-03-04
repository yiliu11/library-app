# Import controllers to make them available at the package level
from .notification_controller import api as notification_ns

# Expose the controllers
__all__ = ['notification_ns']
