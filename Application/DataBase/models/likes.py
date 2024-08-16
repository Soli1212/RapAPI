from .Base import Base
from sqlalchemy import Column, BigInteger ,Integer ,ForeignKey
from sqlalchemy.orm import relationship
class Likes(Base):
    __tablename__ = "likes"
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="Cascade", onupdate="Cascade"), nullable=False, index = True)
    music_id = Column(Integer, ForeignKey("musics.id", ondelete="Cascade", onupdate="Cascade"), nullable=False, index = True)

    users = relationship("Users")
    music = relationship("Musics")