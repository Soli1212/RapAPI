from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.repositories import AlbumRepository
# errors---------------------------------
from Domain.errors.album import NoAlbumFound

class AlbumServices:

    @staticmethod
    async def get_album(db: AsyncSession, album_id: int):
        album = await AlbumRepository.get_album(db, album_id)
        if not album:
            raise NoAlbumFound
        return {
            "album_name": album.album_name,
            "musics_count": album.musics_count,
            "suggested": album.Suggested,
            "new": album.New,
            "album_cover": album.album_cover,
            "artist": {
                "id": album.artists.id,
                "art_name": album.artists.art_name,
                "profile_pic": album.artists.profile_pic
            }, 
            "musics": album.musics,
        }


    @staticmethod # - > change limit
    async def get_new_albums(db: AsyncSession, offset: int, limit: int = 1):
        albums, total_count = await AlbumRepository.get_new_albums(db, limit, offset)
        if not albums:
            raise NoAlbumFound

        total_pages = (total_count + limit - 1) // limit
        return {
            "total_pages": total_pages,
            "albums": [
                {"id": i.id, "album_name": i.album_name, "album_cover": i.album_cover} 
                for i in albums
            ]
        }


    @staticmethod
    async def get_suggested_albums(db: AsyncSession):
        albums = await AlbumRepository.get_suggested_albums(db)
        if not albums:
            raise NoAlbumFound

        return [
            {"id": i.id, "album_name": i.album_name, "album_cover": i.album_cover}
            for i in albums
        ]
