from pydantic import BaseModel
import datetime


class DweetBase(BaseModel):
    body: str


class DweetRetrieve(DweetBase):
    id: int
    created_at: datetime.datetime
    user_id: int

    class Config:
        orm_mode = True
