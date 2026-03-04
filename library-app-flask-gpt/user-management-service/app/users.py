from flask import Blueprint, request, jsonify, g, current_app
from marshmallow import ValidationError
from .schemas import CreateUserRequestSchema, UpdateProfileSchema, StatusPatchSchema, QueryUsersSchema
from .utils import jwt_required, role_required
from .services import UserService
from .errors import APIError

users_bp = Blueprint("users", __name__)
svc = UserService()

# POST /api/users  (create user: librarian only; calls Auth service -> creates local profile)
@users_bp.route("", methods=["POST"])
@jwt_required
@role_required(["librarian"])
def create_user():
    schema = CreateUserRequestSchema()
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as e:
        raise APIError(f"Invalid user data: {e.messages}", status_code=400)

    # Forward caller's JWT to Auth admin/register
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ", 1)[1]
    profile = svc.create_user(creator_token=token, payload=data)
    return jsonify(profile.to_dict()), 201

# GET /api/users (list/search) — librarian only
@users_bp.route("", methods=["GET"])
@jwt_required
@role_required(["librarian"])
def list_users():
    q_schema = QueryUsersSchema()
    try:
        params = q_schema.load({
            "q": request.args.get("q"),
            "role": request.args.get("role"),
            "status": request.args.get("status"),
            "page": request.args.get("page"),
            "size": request.args.get("size")
        })
    except ValidationError as e:
        raise APIError(f"Invalid query: {e.messages}", status_code=400)

    page = params.get("page", 1)
    size = params.get("size") or current_app.config["DEFAULT_PAGE_SIZE"]
    if size > current_app.config["MAX_PAGE_SIZE"]:
        size = current_app.config["MAX_PAGE_SIZE"]

    result = svc.list_users(q=params.get("q"), role=params.get("role"), status=params.get("status"), page=page, size=size)
    return jsonify({
        "total": result["total"],
        "page": result["page"],
        "size": result["size"],
        "items": [p.to_dict() for p in result["items"]]
    }), 200

# GET /api/users/me — current user profile
@users_bp.route("/me", methods=["GET"])
@jwt_required
def me():
    profile = svc.get_profile_by_auth_user(auth_user_id=g.current_user["id"])
    return jsonify(profile.to_dict()), 200

# GET /api/users/<profile_id> — librarian or owner
@users_bp.route("/<profile_id>", methods=["GET"])
@jwt_required
def get_profile(profile_id):
    profile = svc.get_profile_by_id(profile_id)
    if g.current_user["role"] != "librarian" and profile.auth_user_id != g.current_user["id"]:
        raise APIError("Forbidden", status_code=403)
    return jsonify(profile.to_dict()), 200

# PUT /api/users/<profile_id> — update profile; librarian or owner
@users_bp.route("/<profile_id>", methods=["PUT"])
@jwt_required
def update_profile(profile_id):
    schema = UpdateProfileSchema()
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as e:
        raise APIError(f"Invalid profile data: {e.messages}", status_code=400)

    profile = svc.get_profile_by_id(profile_id)
    if g.current_user["role"] != "librarian" and profile.auth_user_id != g.current_user["id"]:
        raise APIError("Forbidden", status_code=403)

    updated = svc.update_profile(profile, data)
    return jsonify(updated.to_dict()), 200

# PATCH /api/users/<profile_id>/status — librarian only
@users_bp.route("/<profile_id>/status", methods=["PATCH"])
@jwt_required
@role_required(["librarian"])
def patch_status(profile_id):
    schema = StatusPatchSchema()
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as e:
        raise APIError(f"Invalid status: {e.messages}", status_code=400)

    profile = svc.get_profile_by_id(profile_id)
    updated = svc.patch_status(profile, data["status"])
    return jsonify(updated.to_dict()), 200
