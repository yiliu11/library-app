from flask import Blueprint, request, jsonify, current_app, g
from .schemas import RegisterSchema, LoginSchema, TokenResponseSchema
from .services import AuthService
from .errors import APIError
from functools import wraps
from .utils import decode_jwt
from .extensions import db
from .models import RevokedToken, User, RoleEnum

auth_bp = Blueprint("auth", __name__)

# Helpers
def get_auth_service():
    return AuthService()

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise APIError("Missing Authorization header", status_code=401)
        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_jwt(token)
        except ValueError as e:
            raise APIError(str(e), status_code=401)
        jti = payload.get("jti")
        if RevokedToken.query.filter_by(jti=jti).first():
            raise APIError("Token revoked", status_code=401)
        # attach user info to g
        g.current_user = User.query.get(payload.get("sub"))
        g.token_payload = payload
        return fn(*args, **kwargs)
    return wrapper

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if not user:
                raise APIError("Authentication required", status_code=401)
            if user.role.value not in allowed_roles:
                raise APIError("Insufficient role", status_code=403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Routes

@auth_bp.route("/register", methods=["POST"])
def register():
    schema = RegisterSchema()
    data = request.get_json() or {}
    try:
        validated = schema.load(data)
    except Exception as e:
        raise APIError(str(e), status_code=400)
    svc = get_auth_service()
    try:
        # Only allow librarians to set role via API in production; here we allow registration but default role enforced in service
        role = validated.get("role", "patron")
        user = svc.register_user(validated["username"], validated["email"], validated["password"], role)
    except ValueError as e:
        raise APIError(str(e), status_code=400)
    return jsonify(user.to_dict()), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    schema = LoginSchema()
    data = request.get_json() or {}
    try:
        validated = schema.load(data)
    except Exception as e:
        raise APIError(str(e), status_code=400)
    svc = get_auth_service()
    try:
        result = svc.login(validated["username"], validated["password"])
    except ValueError as e:
        raise APIError(str(e), status_code=401)
    # Return token (token string, expiry timestamp, role)
    res_schema = TokenResponseSchema()
    return jsonify(res_schema.dump({
        "token": result["token"],
        "expires_in": result["expires_in"],
        "role": result["role"]
    })), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required
def logout():
    payload = getattr(g, "token_payload", {})
    jti = payload.get("jti")
    svc = get_auth_service()
    try:
        svc.revoke_token(jti)
    except ValueError as e:
        raise APIError(str(e), status_code=400)
    return jsonify({"message": "Logged out"}), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required
def me():
    user = getattr(g, "current_user", None)
    if not user:
        raise APIError("User not found", status_code=404)
    return jsonify(user.to_dict()), 200

# Example admin-only endpoint to register users (could be used by librarians)
@auth_bp.route("/admin/register", methods=["POST"])
@jwt_required
@role_required(["librarian"])
def admin_register():
    schema = RegisterSchema()
    data = request.get_json() or {}
    try:
        validated = schema.load(data)
    except Exception as e:
        raise APIError(str(e), status_code=400)
    svc = get_auth_service()
    try:
        user = svc.register_user(validated["username"], validated["email"], validated["password"], validated.get("role", "patron"))
    except ValueError as e:
        raise APIError(str(e), status_code=400)
    return jsonify(user.to_dict()), 201
