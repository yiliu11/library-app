# Import repositories to make them available at the package level
from .book_repository import BookRepository

# Expose the repositories
__all__ = ['BookRepository']
