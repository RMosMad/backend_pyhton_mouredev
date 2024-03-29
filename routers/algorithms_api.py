from enum import Enum
import os
from algorithms import encription_algorithms

from fastapi import APIRouter
from pydantic import BaseModel

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status


router = APIRouter()


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


@router.post('/encryption_algorithms', response_model=EncryptionAlgorithm, status_code=status.HTTP_201_CREATED)
async def create_algorithm(algorithm: EncryptionAlgorithm):
    for algoritmo in algoritmos_disponibles:
        if algoritmo.id == algorithm.id:
            raise HTTPException(status_code=403, detail=f'Algorithm with ID {algorithm.id} already exists')
    algoritmos_disponibles.append(algorithm)
    return algorithm


@router.get('/encryption_algorithms')
async def get_algorithms():
    return algoritmos_disponibles


@router.get('/encryption_algorithms/{algorithm_id}', response_model=EncryptionAlgorithm)
async def get_algorithm(algorithm_id: int):
    for algoritmo in algoritmos_disponibles:
        # if algoritmo['id'] == algorithm_id:
        if algoritmo.id == algorithm_id:
            return algoritmo
    raise HTTPException(status_code=404, detail=f'Algorithm with ID {algorithm_id} not found')


@router.put('/encryption_algorithms/{algorithm_id}', response_model=EncryptionAlgorithm)
async def update_algorithm(algorithm_id: int, algorithm_details: EncryptionAlgorithm):
    for index, algoritmo in enumerate(algoritmos_disponibles):
        if algoritmo.id == algorithm_id:
            algoritmos_disponibles[index] = algorithm_details

            return algorithm_details
    raise HTTPException(status_code=404, detail=f'Algorithm with ID {algorithm_id} not found')


@router.delete('/encryption_algorithms/{algorithm_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_algorithm(algorithm_id: int):
    for index, algorithm in enumerate(algoritmos_disponibles):
        if algorithm.id == algorithm_id:
            algoritmos_disponibles.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f'Algorithm with ID {algorithm_id} not found')


@router.get('/encryption_algorithms/encrypt/{algorithm_id}')
async def encrypt_message(algorithm: AvailableAlgorithms, message: str, t_key: str, key: int = 3):
    encripted_message = ''
    if algorithm is AvailableAlgorithms.reverse_cipher:
        encripted_message = encription_algorithms.reverse_cipher(message)

    if algorithm is AvailableAlgorithms.caesar_cipher:
        encripted_message = encription_algorithms.caesar_cipher(message, key, 'encrypt')

    if algorithm is AvailableAlgorithms.transposition_cipher:
        encripted_message = encription_algorithms.transposition_cipher(message, t_key, 'encrypt')
    return {'encripted_message': encripted_message}


@router.get('/encryption_algorithms/decrypt/{algorithm_id}')
async def decrypt_message(algorithm: AvailableAlgorithms, message: str, t_key: str, key: int = 3):
    encripted_message = ''
    if algorithm is AvailableAlgorithms.reverse_cipher:
        encripted_message = encription_algorithms.reverse_cipher(message)

    if algorithm is AvailableAlgorithms.caesar_cipher:
        encripted_message = encription_algorithms.caesar_cipher(message, key, 'decrypt')

    if algorithm is AvailableAlgorithms.transposition_cipher:
        encripted_message = encription_algorithms.transposition_cipher(message, t_key, 'decrypt')

    return {'encripted_message': encripted_message}





