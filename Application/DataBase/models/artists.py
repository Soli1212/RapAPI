from .Base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .musics import music_artist_association
class Artists(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String, nullable=False)
    art_name = Column(String, unique=True, nullable=False)
    insta_page = Column(String, unique=True, nullable=True)
    generation = Column(Integer, nullable=False, index = True)
    profile_pic = Column(String, unique=True, nullable=True)

    musics = relationship("Musics", secondary = music_artist_association, back_populates="artists")
    albums = relationship("Albums", back_populates="artists")