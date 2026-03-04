# Import routes to make them available at the package level
from .checkout_routes import checkout_bp

# Expose the routes
__all__ = ['checkout_bp']
