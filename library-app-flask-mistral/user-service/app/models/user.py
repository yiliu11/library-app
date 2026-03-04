from app import db
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    PATRON = 'PATRON'
    STAFF = 'STAFF'
    LIBRARIAN = 'LIBRARIAN'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def check_password(self, password, bcrypt):
        return bcrypt.check_password_hash(self.password_hash, password)

    def lock_account(self):
        self.is_active = False
        self.failed_login_attempts = 0

    def increment_failed_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= current_app.config['MAX_FAILED_LOGIN_ATTEMPTS']:
            self.lock_account()

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
