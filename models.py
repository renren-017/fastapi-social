from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()


association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("profiles.id"), primary_key=True),
    Column("right_id", ForeignKey("profiles.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, )


class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    follows = relationship("UserProfile", secondary=association_table)


class Dweet(Base):
    __tablename__ = "dweets"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text,)
    created_at = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey("users.id"))
