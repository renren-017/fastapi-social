from typing import List
from decouple import AutoConfig
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from database import get_db

from .schemas import ProfileSchema
from .models import UserProfile


config = AutoConfig(search_path='/fastapi-social')

router = APIRouter(
    tags=['Profiles'],
    prefix='/profiles'
)


@router.get("/", response_model=List[ProfileSchema])
def get_profile_list(db: Session = Depends(get_db)):
    profiles = db.query(UserProfile).all()
    if not profiles:
        raise HTTPException(status_code=404, detail="Profiles have not been created yet")
    return profiles


@router.get("/{pk}/", response_model=ProfileSchema)
def get_profile_details(pk: int = None, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == pk).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No such profile exists")
    return profile


@router.post("/{pk}/", response_model=ProfileSchema)
def follow_profile(pk: int = None, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == pk).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No such profile exists")
    return profile
