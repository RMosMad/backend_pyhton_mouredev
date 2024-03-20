import os

from routers import algorithms_api, jwt_auth_users

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status


app = FastAPI(debug=True)

app.include_router(algorithms_api.router)
app.include_router(jwt_auth_users.router)


@app.get('/')
async def root():
    return "Hello World from FastAPI. Volume Docker test"


@app.get('/test')
async def test_url():
    return {'url': os. getcwd()}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)





