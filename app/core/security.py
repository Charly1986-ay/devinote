from datetime import datetime, timedelta

import jwt
from pwdlib import PasswordHash

from .config import settings


pwd_context = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hash: str) -> bool:
    return pwd_context.verify(plain, hash)

def create_access_token(data: dict, minutes: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes or settings.JWT_EXPIRES_INT)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])