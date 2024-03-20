import os

from routers import algorithms_api, jwt_auth_users

from fastapi import FastAPI
from pydantic import BaseModel

from redis import Redis

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status


app = FastAPI(debug=True)
redis = Redis(host='redis', port=6379)

app.include_router(algorithms_api.router)
app.include_router(jwt_auth_users.router)


@app.get('/')
async def root():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    
    return f"This webpage has been viewed {counter} time(s)"


@app.get('/test')
async def test_url():
    return {'url': os. getcwd()}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)





