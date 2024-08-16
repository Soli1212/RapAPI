from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.repositories import ArtistRepository
# errors---------------------------------
from Domain.errors.artist import NoArtistFound

class ArtistServices:

    @staticmethod # - > change limit
    async def get_artist_musics(db: AsyncSession, artist_id: int, offset: int, limit: int = 2):
        musics, total_count = await ArtistRepository.get_artist_musics(db, artist_id, offset, limit)
        if musics:
            return {
                "total_pages" : (total_count + limit - 1) // limit,
                "musics" : [{"id": i.id, "Music_name": i.Music_name, "Mucis_cover": i.Mucis_cover} for i in musics]
            }
        else:
            raise NoArtistFound
        
    @staticmethod
    async def get_artist_details(db: AsyncSession, artist_id: int):
        "Get the profile of an artist"

        artist = await ArtistRepository.get_artist_details(db, artist_id)
        if artist:
            return artist
        else:
            raise NoArtistFound


    @staticmethod # - > change limit
    async def get_artists_by_generation(db: AsyncSession, generation: int, offset: int, limit: int = 1):
        "Get artists by generation"
        artists, total_count = await ArtistRepository.get_artists_by_generation(db, generation, limit, offset)
        if artists:
            keys = ["id", "art_name", "profile_pic"]
            return {
                "total_pages" : (total_count + limit - 1) // limit,
                "artists": [dict(zip(keys, artist)) for artist in artists]
            }
        else:
            raise NoArtistFound


    @staticmethod
    async def get_artist_popular_musics(db: AsyncSession, artist_id: int):
        "Getting popular musics from an artist"

        artist = await ArtistRepository.get_artist_popular_musics(db, artist_id)
        if artist and artist.musics:
            return {
                "id": artist.id,
                "art_name": artist.art_name,
                "musics": artist.musics
            }
        else:
            raise NoArtistFound


    @staticmethod
    async def get_artist_suggested_musics(db: AsyncSession, artist_id: int):
        "Getting music suggested by an artist"

        artist = await ArtistRepository.get_artist_suggested_musics(db, artist_id)
        if artist and artist.musics:
            return {
                "id": artist.id,
                "art_name": artist.art_name,
                "musics": artist.musics
            }
        else:
            raise NoArtistFound


    @staticmethod
    async def get_artist_albums(db: AsyncSession, artist_id: int):
        "Getting an artist's albums"

        artist = await ArtistRepository.get_artist_albums(db, artist_id)
        if artist and artist.albums:
            return {
                "id": artist.id,
                "art_name": artist.art_name,
                "albums": artist.albums
            }
        else:
            raise NoArtistFound


    @staticmethod
    async def get_last_artist_album(db: AsyncSession, artist_id: int):
        "Getting the latest album of an artist"

        artist = await ArtistRepository.get_last_artist_album(db, artist_id)
        if artist and artist.albums:
            albums = [{"id": i.id, "album_name": i.album_name, "album_cover": i.album_cover} for i in artist.albums]
            return {
                "id": artist.id,
                "art_name": artist.art_name,
                "albums": albums
            }
        else:
            raise NoArtistFound
