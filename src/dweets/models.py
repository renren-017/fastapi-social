from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime

from database import Base


class Dweet(Base):
    __tablename__ = "dweets"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text,)
    created_at = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey("users.id"))

    class Config:
        orm_mode = True


