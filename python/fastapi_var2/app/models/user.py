import datetime
from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: int | None = None
    email: EmailStr
    name: str
    password: str
    is_bool: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password_check: str
    is_bool: bool = False

    @validator("password_check")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Password don't match")
        return v


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_bool: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime
