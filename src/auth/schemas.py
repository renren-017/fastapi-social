import re

from typing import Union
from fastapi import HTTPException
from pydantic import BaseModel, validator


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


class UserCreateSchema(UserSchema):
    @validator('password')
    def password_validation(cls, value):
        if not re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", value):
            raise HTTPException(
                status_code=422,
                detail="Password must at least 8 characters long "
                       "and contain at least one letter and and one number.")
        return value
