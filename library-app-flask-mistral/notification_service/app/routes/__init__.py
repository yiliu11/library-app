# Import routes to make them available at the package level
from .notification_routes import notification_bp

# Expose the routes
__all__ = ['notification_bp']
