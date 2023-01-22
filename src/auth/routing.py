from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decouple import AutoConfig

from database import get_db, add_to_db
from profiles.models import UserProfile

from .schemas import UserSchema, UserCreateSchema, TokenSchema
from .jwt_handler import encode_token
from .models import User

config = AutoConfig(search_path='/fastapi-social')

router = APIRouter(
    tags=['Auth'],
    prefix='/auth',
)


@router.post("/register/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter_by(username=user.username).first()
    if user_exists:
        raise HTTPException(status_code=409, detail='User with that username already exists in the system.'
                                                    'Try another username')

    db_user = User(
        username=user.username, password=user.password,
    )
    add_to_db(db, db_user)
    db_profile = UserProfile(
        user_id=db_user.id,
    )
    add_to_db(db, db_profile)
    return db_user


@router.post("/token-obtain/", response_model=TokenSchema)
def token_obtain(user: UserSchema, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username == user.username,
                              User.password == user.password).first()
    if u is not None:
        return {
            "access": encode_token(u.id, exp=config("ACCESS_TOKEN_EXP")),
            "refresh": encode_token(u.id, exp=config('REFRESH_TOKEN_EXP'))
        }
    raise HTTPException(
        status_code=401,
        detail='Invalid credentials'
    )
