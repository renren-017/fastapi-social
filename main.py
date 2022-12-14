import uvicorn
from fastapi import FastAPI, Depends, Form
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db

import models
import schema
from models import User, Dweet, UserProfile
from schema import UserSchema, TokenSchema
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/register/", response_model=UserSchema)
def create_user(user: UserSchema):
    db_user = User(
        username=user.username, password=user.password,
    )
    db.session.add(db_user)
    db.session.commit()

    db_profile = UserProfile(
        user_id=db_user.id,
    )
    db.session.add(db_profile)
    db.session.commit()
    return db_user


@app.post("/token-obtain/", response_model=TokenSchema)
def token_obtain(user: UserSchema):
    # userd = User(
    #     username=user.username, password=user.password,
    # )
    u = db.session.query(models.User).filter(models.User.username == user.username).first()
    if u is not None:
        return {
            "access": schema.create_access_token(u.id),
            "refresh": schema.create_refresh_token(u.id)
        }
    return {'Fail': 'BOOOO'}


@app.get("/dashboard/", response_model=schema.DweetSchema)
def get_dweets(user: User = Depends(schema.get_current_user)):
    dweets = db.session.query(models.Dweet).all()
    return dweets


@app.post("/dashboard/", response_model=schema.DweetSchema)
def post_dweets(user: User = Depends(schema.get_current_user), body: str = "No content"):
    db_dweet = Dweet(
        user_id=user.id, body=body
    )
    db.session.add(db_dweet)
    db.session.commit()


@app.get("/profile_list/", response_model=schema.ProfileSchema)
def get_profile_list(user: User = Depends(schema.get_current_user)):
    profiles = db.session.query(models.UserProfile).all()
    return profiles


@app.get("/profile/{pk}", response_model=schema.ProfileSchema)
def get_profile_details(user: User = Depends(schema.get_current_user), pk: int = None):
    profile = db.session.query(models.UserProfile).get(pk=pk)
    return profile


@app.post("/profile/{pk}", response_model=schema.ProfileSchema)
def follow_profile(user: User = Depends(schema.get_current_user), pk: int = None):
    profile = db.session.query(models.UserProfile).get(pk=pk)
    return profile



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
