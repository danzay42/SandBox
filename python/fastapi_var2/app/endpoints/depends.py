from fastapi import Depends, HTTPException, status
from repositories.users import UserRepository
from repositories.items import ItemsRepository
from models.user import User
from core.security import JWTBearer, decode_access_token
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_item_repository() -> ItemsRepository:
    return ItemsRepository(database)


async def get_currnet_user(users: UserRepository = Depends(get_user_repository), token: str = Depends(JWTBearer())) -> User:

    if payload := decode_access_token(token):
        if email := payload.get("sub"):
            if user := await users.get_by_email(email):
                return user
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials aren't valid")
    