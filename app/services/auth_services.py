from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository


class AuthServices:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, playload: UserCreate):
        if self.repo.get_by_email(playload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email ya registrado'
            )
        
        user = User(
            email=playload.email,
            full_name=playload.full_name,
            hashed_password=playload.hashed_password[:72]
        )
        return self.repo.create(user=user)
    
    def login(self, email: str, password: str) -> bool:
        user = self.repo.get_by_email(email=email)

        if not user or not verify_password(password[:72], user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Credenciales inválidas'
            )
        
        token = create_access_token({'sub': str(user.id)})
        return token