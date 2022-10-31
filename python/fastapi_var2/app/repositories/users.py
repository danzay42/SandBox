import datetime
from db.users import users
from models.user import User, UserIn
from core.security import hash_password, verify_password
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all(self, limit: int = 100, skip: int = 0) -> list[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)
    
    async def get_by_id(self, id: int) -> User|None:
        query = users.select().where(users.c.id==id)
        u = await self.database.fetch_one(query=query)
        if u is None:
            return None
        return User.parse_obj(u)

    async def create(self, u: UserIn) -> User:
        user = User(
            name=u.name,
            email=u.email,
            is_bool=u.is_bool,
            password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop("id", None)

        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            name=u.name,
            email=u.email,
            is_bool=u.is_bool,
            password=hash_password(u.password),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop("id", None)
        values.pop("created_at", None)

        query = users.update().where(users.c.id==id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> User|None:
        query = users.select().where(users.c.email==email)
        u = await self.database.fetch_one(query=query)
        if u is None:
            return None
        return User.parse_obj(u)
