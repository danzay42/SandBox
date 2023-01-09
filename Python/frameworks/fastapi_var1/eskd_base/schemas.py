from datetime import date, datetime
from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str
    email: str


class Item(BaseModel):
    dec_no: str
    title: str
    user_id: int
    # origin_dec_no: None | str
    # created: datetime
    # changed: datetime


class ORMItem(Item):
    class Config:
        orm_mode = True


class ORMUser(User):
    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    items: list[ORMItem]

    class Config:
        orm_mode = True


class ShowItem(BaseModel):
    dec_no: str
    title: str
    creator: ORMUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
