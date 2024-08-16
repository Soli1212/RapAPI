from .Base import Base 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, BigInteger
from sqlalchemy.orm import relationship

playlist_music_association = Table(
    'playlist_music_association',
    Base.metadata,
    Column('playlist_id', BigInteger, ForeignKey('playlists.id', ondelete="Cascade", onupdate="Cascade")),
    Column('music_id', BigInteger, ForeignKey('musics.id', ondelete="Cascade", onupdate="Cascade"))
)


class Playlists(Base):
    __tablename__ = "playlists"
    id = Column(BigInteger, primary_key=True, autoincrement = True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, 
        ForeignKey("users.id", ondelete="Cascade", onupdate="Cascade")
    )
    IsPublic = Column(Boolean, default=False, nullable=False)

    users = relationship("Users", back_populates="playlists")
    musics = relationship("Musics", secondary = playlist_music_association)