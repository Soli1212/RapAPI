from .Base import Base 
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, Text
from sqlalchemy.orm import relationship

music_artist_association = Table(
    'music_artist_association',
    Base.metadata,
    Column('music_id', Integer, 
        ForeignKey('musics.id', ondelete="Cascade", onupdate="Cascade"), 
        nullable=False,
    ),
    Column('artist_id', Integer, 
        ForeignKey('artists.id', ondelete="Cascade", onupdate="Cascade"), 
        nullable=False,
        index = True
    )
)


class Musics(Base):
    __tablename__ = "musics"
    id = Column(Integer, primary_key=True, autoincrement=True, index = True)
    Music_name = Column(String, nullable=False, index = True)
    musics_time = Column(String, nullable=False)
    album_id = Column(Integer, 
        ForeignKey("albums.id", ondelete="cascade", onupdate="cascade"), 
        nullable=True
    )
    Music_Content = Column(String, nullable=False, unique=True)
    popular = Column(Boolean, nullable = False, default = False, index = True)
    Suggested = Column(Boolean, nullable=False, default = False, index = True)
    Mucis_cover = Column(String, nullable=False, unique=True)

    artists = relationship("Artists", secondary = music_artist_association, back_populates="musics")
    albums = relationship("Albums", back_populates="musics")
    comments = relationship("Comments", back_populates="musics")