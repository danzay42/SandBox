import datetime
import re
from pydantic import BaseModel, validator
from .user import User, UserOut

class Item(BaseModel):
    id: int | None = None
    dec_no: str
    user: int
    title: str
    is_bool: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ItemIn(BaseModel):
    dec_no: str
    title: str
    is_bool: bool

    @validator("dec_no")
    def validate_decimal_number(cls, v):
        dn_pattern_main = r'[A-ZА-Я]{4}\.\d{6}\.\d{3}'
        dn_pattern_tail = r'(-\d{,3})?'

        match = re.fullmatch(dn_pattern_main+dn_pattern_tail, v)
        if match is None:
            raise ValueError("Bad decimal number")
        print(f"{match=}")
        return match.string
            

class ItemOut(Item):
    # user_r: UserOut
    pass
