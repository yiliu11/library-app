# Import routes to make them available at the package level
from .auth_routes import auth_bp

# Expose the routes
__all__ = ['auth_bp']
