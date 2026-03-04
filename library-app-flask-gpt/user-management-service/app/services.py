from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from flask import current_app, g
from .extensions import db
from .models import UserProfile, RoleEnum, ProfileStatus, UserAudit
from .errors import APIError
from .clients import AuthClient

class UserService:
    def __init__(self):
        self.db = db
        self.auth_client = AuthClient()

    def _audit(self, profile_id: str, action: str, details: str = None):
        audit = UserAudit(user_profile_id=profile_id, actor_user_id=g.current_user["id"], action=action, details=details)
        self.db.session.add(audit)

    def create_user(self, creator_token: str, payload: dict):
        # 1) Create account in Auth Service (credentials & primary user record)
        auth_user = self.auth_client.admin_register(
            token=creator_token,
            username=payload["username"].strip(),
            email=payload["email"].strip().lower(),
            password=payload["password"],
            role=payload["role"]
        )
        # 2) Create local profile linked to Auth user id
        profile = UserProfile(
            auth_user_id=auth_user["id"],
            username=auth_user["username"],
            email=auth_user["email"],
            role=RoleEnum(auth_user["role"]),
            full_name=payload.get("full_name"),
            phone=payload.get("phone"),
            address=payload.get("address"),
            status=ProfileStatus.ACTIVE
        )
        self.db.session.add(profile)
        try:
            self.db.session.commit()
            self._audit(profile.id, "create_user", f"Created by {g.current_user['id']} with role {profile.role.value}")
            self.db.session.commit()
            return profile
        except IntegrityError as e:
            self.db.session.rollback()
            raise APIError("User profile already exists (username/email/auth_user_id)", status_code=409)

    def list_users(self, q: str = None, role: str = None, status: str = None, page: int = 1, size: int = 20):
        query = UserProfile.query
        if q:
            like_term = f"%{q.strip()}%"
            query = query.filter(or_(UserProfile.username.ilike(like_term),
                                     UserProfile.email.ilike(like_term),
                                     UserProfile.full_name.ilike(like_term)))
        if role:
            query = query.filter(UserProfile.role == RoleEnum(role))
        if status:
            query = query.filter(UserProfile.status == ProfileStatus(status))

        total = query.with_entities(func.count()).scalar()
        items = query.order_by(UserProfile.created_at.desc()).offset((page - 1) * size).limit(size).all()
        return {"total": int(total or 0), "page": page, "size": size, "items": items}

    def get_profile_by_id(self, profile_id: str):
        profile = UserProfile.query.get(profile_id)
        if not profile:
            raise APIError("User profile not found", status_code=404)
        return profile

    def get_profile_by_auth_user(self, auth_user_id: str):
        profile = UserProfile.query.filter_by(auth_user_id=auth_user_id).first()
        if not profile:
            raise APIError("User profile not found", status_code=404)
        return profile

    def update_profile(self, target_profile: UserProfile, data: dict):
        if "full_name" in data:
            target_profile.full_name = data["full_name"]
        if "phone" in data:
            target_profile.phone = data["phone"]
        if "address" in data:
            target_profile.address = data["address"]
        try:
            self.db.session.commit()
            self._audit(target_profile.id, "update_profile", f"Updated fields: {list(data.keys())}")
            self.db.session.commit()
            return target_profile
        except Exception:
            self.db.session.rollback
            raise APIError("Failed to update profile", status_code=500)

    def patch_status(self, target_profile: UserProfile, new_status: str):
        target_profile.status = ProfileStatus(new_status)
        try:
            self.db.session.commit()
            self._audit(target_profile.id, "patch_status", f"Status -> {new_status}")
            self.db.session.commit()
            return target_profile
        except Exception:
            self.db.session.rollback()
            raise APIError("Failed to update status", status_code=500)
