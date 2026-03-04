import time
import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from flask import current_app
import uuid

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)

def generate_jwt(payload: dict, exp_seconds: int = None):
    if exp_seconds is None:
        exp_seconds = current_app.config["JWT_EXP_SECONDS"]
    secret = current_app.config["JWT_SECRET"]
    alg = current_app.config["JWT_ALGORITHM"]
    now = int(time.time())
    jti = str(uuid.uuid4())
    token_payload = {
        "iat": now,
        "exp": now + exp_seconds,
        "jti": jti,
        **payload
    }
    token = jwt.encode(token_payload, secret, algorithm=alg)
    return token, token_payload["exp"], jti

def decode_jwt(token: str):
    secret = current_app.config["JWT_SECRET"]
    alg = current_app.config["JWT_ALGORITHM"]
    try:
        payload = jwt.decode(token, secret, algorithms=[alg])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
