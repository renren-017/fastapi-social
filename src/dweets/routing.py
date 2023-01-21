from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decouple import AutoConfig

from database import get_db, add_to_db
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import get_request_user
from auth.models import User

from .schemas import DweetRetrieve, DweetBase
from .models import Dweet


config = AutoConfig(search_path='/fastapi-social')

router = APIRouter(
    tags=['Dweets'],
    prefix='/dweets'
)


@router.get("/", response_model=List[DweetRetrieve])
def get_dweets(db: Session = Depends(get_db)):
    dweets = db.query(Dweet).all()
    return dweets


@router.post("/", response_model=DweetRetrieve, dependencies=[Depends(JWTBearer())])
def post_dweets(body: DweetBase, db: Session = Depends(get_db), user: User = Depends(get_request_user)):
    db_dweet = Dweet(user_id=user.id, body=body.body)
    add_to_db(db, db_dweet)
    return db_dweet
