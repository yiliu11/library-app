# Import models to make them available at the package level
from .user import User, UserRole

# Expose the models
__all__ = ['User', 'UserRole']
