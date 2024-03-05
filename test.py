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
        'active': True,
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

print(users_db)

print('winnie@gmail.com' in users_db)