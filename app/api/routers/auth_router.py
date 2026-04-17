from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DBSession
from app.models.user import UserCreate, UserRead
from app.repositories.user_repository import UserRepository
from app.services.auth_services import AuthServices

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    '/register', 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED
)
def resgister(playload: UserCreate, db: DBSession):
    service = AuthServices(UserRepository(db=db))
    return service.register(playload=playload)


@router.post('/login')
def login(email: str, password: str, db: DBSession):
    service = AuthServices(UserRepository(db=db))
    token = service.login(email=email, password=password)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/token')
def login(db: DBSession, form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    password = form.password
    service = AuthServices(UserRepository(db=db))
    token = service.login(email=email, password=password)
    return {'access_token': token, 'token_type': 'bearer'}