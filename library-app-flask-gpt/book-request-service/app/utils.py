import jwt
from flask import request, jsonify, current_app
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]  

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
            current_user = data
        except Exception as e:
            return jsonify({"error": "Token is invalid!", "details": str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            if current_user.get("role") not in roles:
                return jsonify({"error": "Unauthorized access"}), 403
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator
