from pydantic import BaseModel
from typing import Union


class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class DweetSchema(BaseModel):
    body: str

    class Config:
        orm_mode = True


class ProfileSchema(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access: str
    refresh: str


class TokenData(BaseModel):
    username: Union[str, None] = None