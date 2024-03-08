from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta



ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES  = 1
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'

from starlette.responses import Response
from starlette import status

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=['bcrypt'])


class User(BaseModel):
    id: int
    name: str
    email: str
    description: str | None = None
    active: bool


class UserDB(User):
    password: str


users_list = [
    User(id=1, name='Luz', email='luz@gmail.com', description='Cacheticos', active=True),
    User(id=2, name='Rafael', email='rafael@gmail.com', description='Rafa', active=True),
    User(id=3, name='Ignazio', email='ignazio@gmail.com', description='Nacho', active=True),
    User(id=4, name='Jack', email='jack@gmail.com', description='Perro loco', active=True),
    User(id=5, name='Winnie', email='winnie@gmail.com', description='Perro aún más loco', active=True),
]

users_db = {
    'luz@gmail.com': {
        'id': 1,
        'name': 'Luz',
        'email': 'luz@gmail.com',
        'description': 'Cacheticos',
        'active': True,
        'password': '$2a$12$04Wsa4KK7goJ6KnoUyeCh.TbDJy0/sfgF8y50JmN7RO6lISVeeoYe',  # 123456
    },
    'rafael@gmail.com': {
        'id': 2,
        'name': 'Rafael',
        'email': 'rafael@gmail.com',
        'description': 'Rafa',
        'active': True,
        'password': '$2a$12$04Wsa4KK7goJ6KnoUyeCh.TbDJy0/sfgF8y50JmN7RO6lISVeeoYe',  # 123456
    },
    'ignazio@gmail.com': {
        'id': 3,
        'name': 'Ignazio',
        'email': 'ignazio@gmail.com',
        'description': 'Nacho',
        'active': False,
        'password': '$2a$12$04Wsa4KK7goJ6KnoUyeCh.TbDJy0/sfgF8y50JmN7RO6lISVeeoYe',  # 123456
    },
    'jack@gmail.com': {
        'id': 4,
        'name': 'Jack',
        'email': 'jack@gmail.com',
        'description': 'Perro loco',
        'active': True,
        'password': '$2a$12$deRmrNi1QvkV8JhPJ/QQbeif57ohHULY9d1cdM/U/vt/l5ck1EzzG',  # 123456789
    },
    'winnie@gmail.com': {
        'id': 5,
        'name': 'Winnie',
        'email': 'winnie@gmail.com',
        'description': 'Perro aún más loco',
        'active': True,
        'password': '$2a$12$deRmrNi1QvkV8JhPJ/QQbeif57ohHULY9d1cdM/U/vt/l5ck1EzzG',  # 123456789
    },
}


def search_user(email: str):
    if email in users_db:
        return User(**users_db[email])


def search_user_db(email: str):
    if email in users_db:
        return UserDB(**users_db[email])


async def auth_user(token: str = Depends(oauth2)):

    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Credenciales de autenticación inválidas', headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        email = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('sub')

        if email is None:
            raise credenciales_invalidas

    except JWTError:
        raise credenciales_invalidas

    return search_user(email)


async def current_user(user: User = Depends(auth_user)):
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Usuario inactivo.',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'El usuario {form.username} no se encuentra registrado')

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail=f'Contraseña incorrecta')

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = {
        'sub': user.email, 
        'exp': expire
    }

    return {'access_token': jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), 'token_type': 'bearer'}


@router.get('/users/me')
async def get_me(user: User = Depends(current_user)):
    return user







