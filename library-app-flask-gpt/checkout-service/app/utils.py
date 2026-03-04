from functools import wraps
from flask import request, g, current_app
import jwt
from .errors import APIError

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

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise APIError("Missing Authorization header", status_code=401)
        token = auth_header.split(" ", 1)[1]
        payload = decode_jwt(token)
        # attach to g
        g.current_user = {
            "id": payload.get("sub"),
            "username": payload.get("username"),
            "role": payload.get("role")
        }
        g.token_payload = payload
        return fn(*args, **kwargs)
    return wrapper

def role_allowed(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if not user:
                raise APIError("Authentication required", status_code=401)
            if user.get("role") not in allowed_roles:
                raise APIError("Insufficient role", status_code=403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
