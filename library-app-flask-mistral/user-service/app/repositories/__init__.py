# Import repositories to make them available at the package level
from .user_repository import UserRepository

# Expose the repositories
__all__ = ['UserRepository']
