from typing import Union

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access: str
    refresh: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
