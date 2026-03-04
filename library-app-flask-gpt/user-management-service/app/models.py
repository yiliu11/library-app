import uuid
from datetime import datetime
import enum
from .extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class RoleEnum(enum.Enum):
    PATRON = "patron"
    STAFF = "staff"
    LIBRARIAN = "librarian"

class ProfileStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"

class UserProfile(db.Model):
    __tablename__ = "user_profiles"
    id = db.Column(db.String, primary_key=True, default=gen_uuid)
    auth_user_id = db.Column(db.String, nullable=False, unique=True, index=True)  # FK to Auth Service user id
    username = db.Column(db.String(128), nullable=False, unique=True, index=True)
    email = db.Column(db.String(256), nullable=False, unique=True, index=True)

    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.PATRON)

    full_name = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(512), nullable=True)

    status = db.Column(db.Enum(ProfileStatus), nullable=False, default=ProfileStatus.ACTIVE)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "auth_user_id": self.auth_user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "full_name": self.full_name,
            "phone": self.phone,
            "address": self.address,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class UserAudit(db.Model):
    __tablename__ = "user_audit"
    id = db.Column(db.String, primary_key=True, default=gen_uuid)
    user_profile_id = db.Column(db.String, db.ForeignKey("user_profiles.id"), nullable=False, index=True)
    actor_user_id = db.Column(db.String, nullable=False)  # who did the action (auth user id)
    action = db.Column(db.String(64), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
