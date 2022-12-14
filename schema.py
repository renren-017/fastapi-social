from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from main import db
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from pydantic import ValidationError


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

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = "notasecwet"
JWT_REFRESH_SECRET_KEY = "secwet"


def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/register/",
    scheme_name="JWT"
)


class TokenData(BaseModel):
    username: Union[str, None] = None


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserSchema:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        token_data = TokenData(username=username)

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = db.get(payload.sub, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserSchema(**user)