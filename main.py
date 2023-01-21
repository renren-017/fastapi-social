import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from decouple import config, AutoConfig
from typing import List

from app.database import get_db, add_to_db, Base, engine
from app.models import User, Dweet, UserProfile
from app.schema import UserSchema, TokenSchema, DweetBase, DweetRetrieve, TokenData, ProfileSchema
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import get_request_user, encode_token, decode_token
Base.metadata.create_all(bind=engine)
config = AutoConfig(search_path='/fastapi-social')

app = FastAPI()


@app.post("/register/", response_model=UserSchema, tags=["auth"])
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username, password=user.password,
    )
    add_to_db(db, db_user)
    db_profile = UserProfile(
        user_id=db_user.id,
    )
    add_to_db(db, db_profile)
    return db_user


@app.post("/token-obtain/", response_model=TokenSchema, tags=["auth"])
def token_obtain(user: UserSchema, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username == user.username).first()
    if u is not None:
        return {
            "access": encode_token(u.id, exp=config("ACCESS_TOKEN_EXP")),
            "refresh": encode_token(u.id, exp=config('REFRESH_TOKEN_EXP'))
        }
    return {'Detail': f'User with id {user.id} was not found in the system. '
                      'Consider registering again or contact Help Center'}


@app.get("/dashboard/", response_model=List[DweetRetrieve], tags=["dweets"])
def get_dweets(db: Session = Depends(get_db)):
    dweets = db.query(Dweet).all()
    return dweets


@app.post("/dashboard/", response_model=DweetRetrieve, dependencies=[Depends(JWTBearer())], tags=["dweets"])
def post_dweets(body: DweetBase, db: Session = Depends(get_db), user: User = Depends(get_request_user)):
    db_dweet = Dweet(user_id=user.id, body=body.body)
    add_to_db(db, db_dweet)
    return db_dweet


@app.get("/profile_list/", response_model=List[ProfileSchema], tags=["profiles"])
def get_profile_list(db: Session = Depends(get_db)):
    profiles = db.query(UserProfile).all()
    if not profiles:
        raise HTTPException(status_code=404, detail="Profiles have not been created yet")
    return profiles


@app.get("/profile/{pk}", response_model=ProfileSchema, tags=["profiles"])
def get_profile_details(pk: int = None, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == pk).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No such profile exists")
    return profile


@app.post("/profile/{pk}", response_model=ProfileSchema, tags=["profiles"])
def follow_profile(pk: int = None, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == pk).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No such profile exists")
    return profile


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
