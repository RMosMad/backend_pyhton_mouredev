from enum import Enum
import os
import encription_algorithms

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class EncryptionAlgorithm(BaseModel):
    id: int
    name: str
    code: str
    description: str | None = None


algoritmos_disponibles = [
    EncryptionAlgorithm(id=1, name='Reverse Cipher', code='reverse_cipher', description='The reverse cipher encrypts a message by printing it in reverse order'),
    EncryptionAlgorithm(id=2, name='Caesar Cipher', code='caesar_cipher', description='The Caesar cipher works by substituting each letter of a message with a new letter after shifting the alphabet over'),
    EncryptionAlgorithm(id=3, name='Transposition Cipher', code='transposition_cipher', description='Given a plain-text message and a numeric key, cipher/de-cipher the given text using Columnar Transposition Cipher'),
]


class AvailableAlgorithms(str, Enum):
    reverse_cipher = 'reverse_cipher'
    caesar_cipher = 'caesar_cipher'
    transposition_cipher = 'transposition_cipher'


@app.get('/')
async def root():
    return "Hello World from FastAPI"


@app.get('/test')
async def test_url():
    return {'url': os. getcwd()}


@app.get('/encryption_algorithms')
async def encryption_algorithms():
    return algoritmos_disponibles


@app.get('/encryption_algorithms/encrypt/{algorithm_id}')
async def encrypt_message(algorithm: AvailableAlgorithms, message: str, t_key: str, key: int = 3):
    encripted_message = ''
    if algorithm is AvailableAlgorithms.reverse_cipher:
        encripted_message = encription_algorithms.reverse_cipher(message)

    if algorithm is AvailableAlgorithms.caesar_cipher:
        encripted_message = encription_algorithms.caesar_cipher(message, key, 'encrypt')

    if algorithm is AvailableAlgorithms.transposition_cipher:
        encripted_message = encription_algorithms.transposition_cipher(message, t_key, 'encrypt')
    return {'encripted_message': encripted_message}


@app.get('/encryption_algorithms/decrypt/{algorithm_id}')
async def decrypt_message(algorithm: AvailableAlgorithms, message: str, t_key: str, key: int = 3):
    encripted_message = ''
    if algorithm is AvailableAlgorithms.reverse_cipher:
        encripted_message = encription_algorithms.reverse_cipher(message)

    if algorithm is AvailableAlgorithms.caesar_cipher:
        encripted_message = encription_algorithms.caesar_cipher(message, key, 'decrypt')

    if algorithm is AvailableAlgorithms.transposition_cipher:
        encripted_message = encription_algorithms.transposition_cipher(message, t_key, 'decrypt')

    return {'encripted_message': encripted_message}







