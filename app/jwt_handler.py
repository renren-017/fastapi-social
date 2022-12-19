import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

JWT_ACCESS_EXP = os.environ['ACCESS_TOKEN_EXP']
JWT_REFRESH_EXP = os.environ['REFRESH_TOKEN_EXP']
JWT_ALGORITHM = os.environ['ALGORITHM']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']


def encode_token(subject: Union[str, Any], exp: str) -> str:
    expires_delta = datetime.now() + timedelta(minutes=int(exp))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return decoded_token if decoded_token["expires"] >= datetime.now() else None


def verify_jwt(self, token: str) -> bool:
    is_token_valid: bool = False
    payload = decode_token(token)
    if payload:
        is_token_valid = True
    return is_token_valid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def get_request_user(token: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = None) -> User:
    token = token.credentials
    try:
        payload = decode_token(token)
        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(status_code=401, detail='Token has expired', headers={"WWW-Authenticate": "Bearer"})

    except ValidationError:
        raise HTTPException(
            status_code=403, detail='Invalid token', headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.get(User, payload['sub'])
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Пользователь не найден'
        )
    return user