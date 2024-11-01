from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.repositories import MusicRepository
from Domain.errors.music import NoMusicFound

class MusicServices:
    @staticmethod
    async def get_music_by_id(db: AsyncSession, music_id: int):
        music = await MusicRepository.get_music_by_id(db, music_id)
        if music:
            album = {
                "id": music.albums.id, 
                "album_name": music.albums.album_name, 
                "album_cover": music.albums.album_cover
            } if music.albums else None

            return {
                "Music_name": music.Music_name,
                "musics_time": music.musics_time,
                "popular": music.popular,
                "Suggested": music.Suggested,   
                "Music_Content": music.Music_Content,
                "Mucis_cover": music.Mucis_cover,
                "artists": music.artists,
                "album": album
            }
        else:
            raise NoMusicFound


    @staticmethod # - > change limit
    async def get_popular_musics(db: AsyncSession, offset: int, limit: int = 1):
        musics, total_count = await MusicRepository.get_popular_musics(db, limit, offset)
        if musics:
            return {
                "total_count": (total_count + limit - 1) // limit,
                "Musics": [
                    {"id": i.id, "Music_name": i.Music_name, "Mucis_cover": i.Mucis_cover} 
                    for i in musics
                ]
            }
        else:
            raise NoMusicFound


    @staticmethod # - > change limit
    async def get_suggested_musics(db: AsyncSession, offset: int, limit: int = 1):
        musics, total_count = await MusicRepository.get_suggested_musics(db, limit, offset)
        if musics:
            return {
                "total_count": (total_count + limit - 1) // limit,
                "Musics": [
                    {"id": i.id, "Music_name": i.Music_name, "Mucis_cover": i.Mucis_cover} 
                    for i in musics
                ]
            }
        else:
            raise NoMusicFound
