from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import current_app
from .extensions import db
from .models import User, FailedLogin, RevokedToken, RoleEnum
from .utils import hash_password, verify_password, generate_jwt

class AuthService:
    def __init__(self):
        self.db = db
        self.max_attempts = current_app.config["MAX_LOGIN_ATTEMPTS"]
        self.lockout_seconds = current_app.config["LOCKOUT_SECONDS"]

    def register_user(self, username: str, email: str, password: str, role: str = "patron"):
        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            raise ValueError("Username or email already exists")

        user = User(
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=hash_password(password),
            role=RoleEnum(role)
        )
        self.db.session.add(user)
        try:
            self.db.session.commit()
            return user
        except IntegrityError:
            self.db.session.rollback()
            raise ValueError("Failed to create user due to integrity error")

    def _get_failed_login(self, username):
        fl = FailedLogin.query.filter_by(username=username).first()
        if not fl:
            fl = FailedLogin(username=username)
            self.db.session.add(fl)
            self.db.session.commit()
        return fl

    def login(self, username: str, password: str):
        username = username.strip()
        user = User.query.filter_by(username=username).first()
        if not user:
            # register a failed attempt even if user not found to impede enumeration
            fl = self._get_failed_login(username)
            fl.mark_attempt(self.lockout_seconds, self.max_attempts)
            self.db.session.commit()
            raise ValueError("Invalid credentials")

        fl = self._get_failed_login(username)
        if fl.locked_until and fl.locked_until > datetime.utcnow():
            raise ValueError("Account locked. Try again later.")

        if not verify_password(password, user.password_hash):
            fl.mark_attempt(self.lockout_seconds, self.max_attempts)
            self.db.session.commit()
            raise ValueError("Invalid credentials")

        # success -> reset failed attempts
        fl.reset()
        self.db.session.commit()

        # generate JWT
        payload = {
            "sub": user.id,
            "username": user.username,
            "role": user.role.value
        }
        token, exp_ts, jti = generate_jwt(payload)
        return {"token": token, "expires_in": exp_ts, "role": user.role.value, "jti": jti}

    def revoke_token(self, jti: str):
        if not jti:
            raise ValueError("Missing token id")
        rt = RevokedToken(jti=jti)
        self.db.session.add(rt)
        self.db.session.commit()
        return True

    def is_token_revoked(self, jti: str):
        return RevokedToken.query.filter_by(jti=jti).first() is not None

    def get_user_by_id(self, user_id: str):
        return User.query.get(user_id)
