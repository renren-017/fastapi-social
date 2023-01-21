from pydantic import BaseModel
from typing import Union
import datetime

from app.models import Dweet


class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class DweetBase(BaseModel):
    body: str


class DweetRetrieve(DweetBase):
    id: int
    created_at: datetime.datetime
    user_id: int

    class Config:
        orm_mode = True


# class DweetResponseSchema(Dweet):
#     class Config:
#         orm_mode = True



class ProfileSchema(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access: str
    refresh: str


class TokenData(BaseModel):
    username: Union[str, None] = None