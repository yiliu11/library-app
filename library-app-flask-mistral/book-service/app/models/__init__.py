# Import models to make them available at the package level
from .book import Book, AvailabilityStatus

# Expose the models
__all__ = ['Book', 'AvailabilityStatus']
