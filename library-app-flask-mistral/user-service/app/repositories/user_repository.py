from app import db
from app.models.user import User, UserRole
from werkzeug.exceptions import NotFound, Conflict

class UserRepository:
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise NotFound('User not found')
        return user

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(username, email, password_hash, role):
        if User.query.filter_by(username=username).first():
            raise Conflict('Username already exists')
        if User.query.filter_by(email=email).first():
            raise Conflict('Email already exists')

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=UserRole[role]
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user):
        db.session.commit()
        return user

    @staticmethod
    def lock_user(user):
        user.lock_account()
        db.session.commit()
        return user
