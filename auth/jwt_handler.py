from decouple import config, AutoConfig
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

config = AutoConfig(search_path='/fastapi-social')

JWT_ACCESS_EXP = config('ACCESS_TOKEN_EXP')
JWT_REFRESH_EXP = config('REFRESH_TOKEN_EXP')
JWT_ALGORITHM = config('JWT_ALGORITHM')
JWT_SECRET_KEY = config('JWT_SECRET_KEY')


def encode_token(subject: Union[str, Any], exp: str) -> str:
    to_encode = {
        "exp": datetime.now() + timedelta(minutes=int(exp)),
        "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    try:
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None


def verify_jwt(token: str) -> bool:
    is_token_valid: bool = False
    payload = decode_token(token)
    if payload:
        is_token_valid = True
    return is_token_valid


def get_request_user(token: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db)) -> User:
    token = token.credentials
    try:
        payload = decode_token(token)
        print(payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail='Token has expired', headers={"WWW-Authenticate": "Bearer"}
        )
    except ValidationError:
        raise HTTPException(
            status_code=403, detail='Invalid token', headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.id == payload['sub']).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user