from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    class Config:
        orm_mode = True


class Follow(Base):
    __tablename__ = 'followers'

    id = Column(Integer, primary_key=True, index=True)
    following_id = Column(Integer, ForeignKey("profiles.id", ondelete='CASCADE'))
    follower_id = Column(Integer, ForeignKey("profiles.id", ondelete='CASCADE'))

    following = relationship("UserProfile", backref='following', foreign_keys=[following_id])
    followers = relationship("UserProfile", backref='followers', foreign_keys=[follower_id])
