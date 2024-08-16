from .Base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)

    playlists = relationship("Playlists", back_populates="users")