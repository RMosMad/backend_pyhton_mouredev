from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')


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
        'password': '123456',
    },
    'rafael@gmail.com': {
        'id': 2,
        'name': 'Rafael',
        'email': 'rafael@gmail.com',
        'description': 'Rafa',
        'active': True,
        'password': '123456',
    },
    'ignazio@gmail.com': {
        'id': 3,
        'name': 'Ignazio',
        'email': 'ignazio@gmail.com',
        'description': 'Nacho',
        'active': False,
        'password': '123456',
    },
    'jack@gmail.com': {
        'id': 4,
        'name': 'Jack',
        'email': 'jack@gmail.com',
        'description': 'Perro loco',
        'active': True,
        'password': '123456',
    },
    'winnie@gmail.com': {
        'id': 5,
        'name': 'Winnie',
        'email': 'winnie@gmail.com',
        'description': 'Perro aún más loco',
        'active': True,
        'password': '123456',
    },
}


def search_user(email: str):
    if email in users_db:
        return User(**users_db[email])


def search_user_db(email: str):
    if email in users_db:
        return UserDB(**users_db[email])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'No autorizado', headers={'WWW-Authenticate': 'Bearer'}
        )
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
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail=f'Contraseña incorrecta')

    return {'access_token': user.email, 'token_type': 'bearer'}


@router.get('/')
async def root():
    return "Users Authentication API"


@router.get('/users/me')
async def get_me(user: User = Depends(current_user)):
    return user


@router.post('/users', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_id: User):
    for user in users_list:
        if user.id == user_id.id:
            raise HTTPException(status_code=403, detail=f'Algorithm with ID {user_id.id} already exists')
    users_list.append(user_id)
    return user_id


@router.get('/users')
async def get_users():
    return users_list


@router.get('/users/{user_id}', response_model=User)
async def get_user(user_id: int):
    for user in users_list:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail=f'Algorithm with ID {user_id} not found')


@router.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, user_details: User):
    for index, user in enumerate(users_list):
        if user.id == user_id:
            users_list[index] = user_details

            return user_details
    raise HTTPException(status_code=404, detail=f'Algorithm with ID {user_id} not found')


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_algorithm(user_id: int):
    for index, user in enumerate(users_list):
        if user.id == user_id:
            users_list.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f'Algorithm with ID {user_id} not found')










