from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, )


class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class Dweet(Base):
    __tablename__ = "dweets"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text,)
    created_at = Column(DateTime, default=datetime.now())

    user_id = Column(Integer, ForeignKey("users.id"))


class Follow(Base):
    __tablename__ = 'followers'

    id = Column(Integer, primary_key=True, index=True)
    following_id = Column(Integer, ForeignKey("profiles.id", ondelete='CASCADE'))
    follower_id = Column(Integer, ForeignKey("profiles.id", ondelete='CASCADE'))

    following = relationship("UserProfile", backref='following', foreign_keys=[following_id])
    followers = relationship("UserProfile", backref='followers', foreign_keys=[follower_id])
