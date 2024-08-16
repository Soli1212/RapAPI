#---------------------------------
from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.repositories import PlaylistRepository
from Application.DataBase.repositories import MusicRepository
#errors--------------------------
from Domain.errors.playlist import PlaylistLimit
from Domain.errors.playlist import PlaylistNotExists
from Domain.errors.playlist import AvailableMusic
from Domain.errors.playlist import NotAvailableMusic
from Domain.errors.music import NoMusicFound

class PlaylistServices:
    @staticmethod
    async def create_playlist(db: AsyncSession, name: str, user_id: int, IsPublic: bool = False):
        UserPlayListCount = await PlaylistRepository.count_user_playlists(db, user_id)
        if UserPlayListCount == 5:
            raise PlaylistLimit
        if X := await PlaylistRepository.create_playlist(db, name = name, user_id = user_id, IsPublic = IsPublic):
            return {"message" : "Playlist successfully created"}


    @staticmethod
    async def delete_playlist(db: AsyncSession, playlist_id: int, user_id: int):
        if playlist := await PlaylistRepository.Get_playlist_with_access(db, user_id, playlist_id):
            if await PlaylistRepository.delete_playlist(db, playlist):
                return {"message" : "Playlist was successfully deleted"}
        else:
            raise PlaylistNotExists
        

    @staticmethod
    async def update_playlist(db: AsyncSession, playlist_id: int, user_id: int, name: str = None, IsPublic: bool = None):
        playlist = await PlaylistRepository.Get_playlist_with_access(db, user_id, playlist_id)
        if not playlist:
            raise PlaylistNotExists
        if name != None:
            playlist.name = name
        if IsPublic != None:
            playlist.IsPublic = IsPublic
        if name is not None or IsPublic is not None:
            return {"message" : "Playlist was successfully updated"}
    

    @staticmethod
    async def add_music_to_playlist(db: AsyncSession, playlist_id: int, music_id: int, user_id: int):
        if not await PlaylistRepository.Get_playlist_with_access(db, user_id, playlist_id):
            raise PlaylistNotExists
        if await PlaylistRepository.check_exist_music_in_playlist(db, playlist_id, music_id):
            raise AvailableMusic
        if not await MusicRepository.get_short_music_data(db, music_id):
            raise NoMusicFound
        if await PlaylistRepository.add_music_to_playlist(db, playlist_id, music_id):
            return {"message" : "Music successfully added to playlist"}
        

    @staticmethod
    async def delete_music_to_playlist(db: AsyncSession, playlist_id: int, music_id: int, user_id: int):
        if not await PlaylistRepository.Get_playlist_with_access(db, user_id, playlist_id):
            raise PlaylistNotExists
        if await PlaylistRepository.check_exist_music_in_playlist(db, playlist_id, music_id):
            if await PlaylistRepository.delete_music_to_playlist(db, playlist_id, music_id):
                return {"message" : "Music has been successfully removed from the playlist"}
        else : 
            raise NotAvailableMusic
        

    @staticmethod
    async def my_playlists(db: AsyncSession, user_id: int):
        if playlists := await PlaylistRepository.my_playlists(db, user_id):
            return [{"id": i.id, "name": i.name} for i in playlists]
        else:
            raise PlaylistNotExists
        

    @staticmethod # - > change limit
    async def get_my_playlist(db: AsyncSession, user_id: int, playlist_id: int, offset: int, limit: int = 1):
        if await PlaylistRepository.Get_playlist_with_access(db, user_id, playlist_id):
            musics, total_count = await PlaylistRepository.get_playlist(db, playlist_id, limit, offset)
            if not musics:
                raise NoMusicFound
            return {
                "total_pages" : (total_count + limit - 1) // limit,
                "musics" : [{"id": music.id, "Music_name": music.Music_name, "Mucis_cover": music.Mucis_cover} for music in musics]
            }
        else:
            raise PlaylistNotExists


    @staticmethod # - > change limit
    async def get_public_playlist(db: AsyncSession, playlist_id: int, offset: int, limit: int = 1):
        if playlist := await PlaylistRepository.check_IsPublic(db, playlist_id):
            musics, total_count = await PlaylistRepository.get_playlist(db, playlist_id, limit, offset)
            if not musics:
                raise NoMusicFound
            return {
                "total_pages" : (total_count + limit - 1) // limit,
                "playlis_data": {
                    "name": playlist.name,
                    "user": {
                        "id": playlist.users.id,
                        "name": playlist.users.name,
                        "profile_pic": playlist.users.profile_pic
                    }
                },
                "musics" : [{"id": music.id, "Music_name": music.Music_name, "Mucis_cover": music.Mucis_cover} for music in musics]
            }
        else:
            raise PlaylistNotExists
        