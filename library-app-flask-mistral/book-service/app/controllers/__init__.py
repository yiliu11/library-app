# Import controllers to make them available at the package level
from .book_controller import api as book_ns

# Expose the controllers
__all__ = ['book_ns']
