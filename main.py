import uvicorn
import os
import jwt_handler
import models
import schema
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import get_db, add_to_db
from app.models import User, Dweet, UserProfile
from app.schema import UserSchema, TokenSchema

from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()


@app.post("/register/", response_model=UserSchema, tags=["auth"])
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username, password=user.password,
    )
    db_profile = UserProfile(
        user_id=db_user.id,
    )
    add_to_db(db, db_user, db_profile)
    return db_user


@app.post("/token-obtain/", response_model=TokenSchema, tags=["auth"])
def token_obtain(user: UserSchema, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.username == user.username).first()
    if u is not None:
        return {
            "access": jwt_handler.encode_token(u.id, exp=os.environ["ACCESS_TOKEN_EXP"]),
            "refresh": jwt_handler.encode_token(u.id, exp=os.environ['REFRESH_TOKEN_EXP'])
        }
    return {'Fail': 'BOOOO'}


@app.get("/dashboard/", response_model=schema.DweetSchema, tags=["dweets"])
def get_dweets(db: Session = Depends(get_db)):
    dweets = db.query(models.Dweet).all()
    return dweets


@app.post("/dashboard/", response_model=schema.DweetSchema, dependencies=[Depends(jwt_handler.JWTBearer())],
          tags=["dweets"])
def post_dweets(body: str = "No content",
                db: Session = Depends(get_db),
                user: User = Depends(jwt_handler.get_request_user)):
    db_dweet = Dweet(
        user_id=user.id, body=body
    )
    db.add(db_dweet)
    db.commit()


@app.get("/profile_list/", response_model=schema.ProfileSchema, tags=["profiles"])
def get_profile_list(db: Session = Depends(get_db)):
    profiles = db.query(models.UserProfile).all()
    return profiles


@app.get("/profile/{pk}", response_model=schema.ProfileSchema, tags=["profiles"])
def get_profile_details(pk: int = None, db: Session = Depends(get_db)):
    profile = db.query(models.UserProfile).get(id=pk)
    return profile


@app.post("/profile/{pk}", response_model=schema.ProfileSchema, tags=["profiles"])
def follow_profile(pk: int = None, db: Session = Depends(get_db)):
    profile = db.query(models.UserProfile).get(id=pk)
    return profile


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
