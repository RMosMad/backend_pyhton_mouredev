from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette.responses import Response
from starlette import status

app = FastAPI(debug=True)

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










