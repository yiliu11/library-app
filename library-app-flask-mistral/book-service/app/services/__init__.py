# Import services to make them available at the package level
from .book_service import BookService

# Expose the services
__all__ = ['BookService']
