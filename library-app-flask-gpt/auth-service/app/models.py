import enum
import uuid
from datetime import datetime, timedelta

from .extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class RoleEnum(enum.Enum):
    PATRON = "patron"
    STAFF = "staff"
    LIBRARIAN = "librarian"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True, default=gen_uuid)
    username = db.Column(db.String(128), unique=True, nullable=False, index=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.PATRON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at.isoformat(),
        }

class FailedLogin(db.Model):
    __tablename__ = "failed_logins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, index=True)
    attempts = db.Column(db.Integer, default=0, nullable=False)
    last_attempt_at = db.Column(db.DateTime, default=datetime.utcnow)
    locked_until = db.Column(db.DateTime, nullable=True)

    def mark_attempt(self, lockout_seconds, max_attempts):
        from datetime import datetime, timedelta
        self.attempts += 1
        self.last_attempt_at = datetime.utcnow()
        if self.attempts >= max_attempts:
            self.locked_until = datetime.utcnow() + timedelta(seconds=lockout_seconds)

    def reset(self):
        self.attempts = 0
        self.last_attempt_at = datetime.utcnow()
        self.locked_until = None

class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(128), unique=True, nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
