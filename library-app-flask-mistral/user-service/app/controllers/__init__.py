# Import controllers to make them available at the package level
from .auth_controller import api as auth_ns

# Expose the controllers
__all__ = ['auth_ns']
