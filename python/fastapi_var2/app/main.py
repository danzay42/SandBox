import uvicorn
from fastapi import FastAPI
from db.base import database
from endpoints import users, auth, items


app = FastAPI(title="Another version of fastapi application")
app.include_router(auth.router, prefix="/login", tags=["JWT Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])


@app.on_event("startup")
async def db_up():
    await database.connect()


@app.on_event("shutdown")
async def db_down():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
