from fastapi import FastAPI, responses
from . import models, database
from .routers import users, items, authentication

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
def index():
    return responses.FileResponse('static/index.html')
