
from fastapi import FastAPI
from api import api

app = FastAPI(debug=True)


# Routers
app.include_router(api.router)

