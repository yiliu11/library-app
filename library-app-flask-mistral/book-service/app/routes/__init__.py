# Import routes to make them available at the package level
from .book_routes import book_bp

# Expose the routes
__all__ = ['book_bp']
