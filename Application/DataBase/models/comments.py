from .Base import Base
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Text
from sqlalchemy.orm import relationship
class Comments(Base):
    __tablename__ = "comments"
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    content = Column(Text, nullable=False, unique=False)
    user_id = Column(Integer, 
        ForeignKey("users.id", ondelete="Cascade", onupdate="Cascade"), 
        nullable=False,
        index = True
    )
    music_id = Column(Integer,
        ForeignKey("musics.id", ondelete="Cascade", onupdate="Cascade"),
        nullable=False,
        index = True
    )

    user = relationship("Users")
    musics = relationship("Musics", back_populates="comments")