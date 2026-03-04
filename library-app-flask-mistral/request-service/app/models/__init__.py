# Import models to make them available at the package level
from .request import BookRequest, RequestStatus

# Expose the models
__all__ = ['BookRequest', 'RequestStatus']
