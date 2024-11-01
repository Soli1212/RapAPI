from .Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Albums(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True, autoincrement=True, index = True)
    album_name = Column(String, nullable=False)
    musics_count = Column(Integer, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="Cascade", onupdate="Cascade"), nullable=False)
    New = Column(Boolean, nullable = False, default = False, index=True)
    Suggested = Column(Boolean, nullable=False, default = False, index=True)
    album_cover = Column(String, nullable = False, unique = True)

    artists = relationship("Artists", back_populates="albums")
    musics = relationship("Musics", back_populates="albums")