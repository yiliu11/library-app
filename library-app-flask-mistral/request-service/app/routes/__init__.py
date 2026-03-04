# Import routes to make them available at the package level
from .request_routes import request_bp

# Expose the routes
__all__ = ['request_bp']
