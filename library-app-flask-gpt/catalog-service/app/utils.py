import jwt
import time
from flask import current_app, request, g
from functools import wraps
from .errors import APIError

# Role enum values (must match values used by Auth Service)
ROLE_PATRON = "patron"
ROLE_STAFF = "staff"
ROLE_LIBRARIAN = "librarian"

def decode_jwt(token: str):
    secret = current_app.config["JWT_SECRET"]
    alg = current_app.config["JWT_ALGORITHM"]
    try:
        payload = jwt.decode(token, secret, algorithms=[alg])
        return payload
    except jwt.ExpiredSignatureError:
        raise APIError("Token expired", status_code=401)
    except jwt.InvalidTokenError:
        raise APIError("Invalid token", status_code=401)

def jwt_optional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            payload = decode_jwt(token)
            g.current_token = payload
        else:
            g.current_token = None
        return fn(*args, **kwargs)
    return wrapper

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise APIError("Missing Authorization header", status_code=401)
        token = auth_header.split(" ", 1)[1]
        payload = decode_jwt(token)
        # Optionally: check token revocation via Auth service (not implemented here)
        g.current_token = payload
        return fn(*args, **kwargs)
    return wrapper

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = getattr(g, "current_token", None)
            if not token:
                raise APIError("Authentication required", status_code=401)
            role = token.get("role")
            if role not in allowed_roles:
                raise APIError("Insufficient role", status_code=403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
