from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
#-----------------------------------
from Application.DataBase.models import Artists, Musics, Albums
from Application.DataBase.models.artists import music_artist_association

class ArtistRepository:
    
    async def get_artist_musics(db: AsyncSession, artist_id: int, offset: int, limit: int):
        count_query = select(func.count(music_artist_association.c.music_id)).where(
            music_artist_association.c.artist_id == artist_id
        )
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = (
            select(Musics.id, Musics.Music_name, Musics.Mucis_cover)
            .join(music_artist_association, Musics.id == music_artist_association.c.music_id)
            .filter(music_artist_association.c.artist_id == artist_id)
            .offset(offset * limit)
            .limit(limit)
        )

        result = await db.execute(query)
        return result.fetchall(), total_count

    async def get_artists_by_generation(db: AsyncSession, generation: int, limit: int, offset: int):
        count_query = select(func.count(Artists.id)).where(
            Artists.generation == generation
        )
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = select(Artists.id, Artists.art_name, Artists.profile_pic).filter(
            Artists.generation == generation
        ).limit(limit).offset(limit * offset)
        result = await db.execute(query)
        return result.fetchall(), total_count

    async def get_artist_details(db: AsyncSession, artist_id: int):
        query = select(Artists).filter(Artists.id == artist_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_artist_popular_musics(db: AsyncSession, artist_id: int):
        query = select(Artists).options(
            joinedload(Artists.musics.and_(Musics.popular == True)).load_only(Musics.id, Musics.Music_name, Musics.Mucis_cover)
        ).filter(Artists.id == artist_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_artist_suggested_musics(db: AsyncSession, artist_id: int):
        query = select(Artists).options(
            joinedload(Artists.musics.and_(Musics.Suggested == True)).load_only(Musics.id, Musics.Music_name, Musics.Mucis_cover)
        ).filter(Artists.id == artist_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_artist_albums(db: AsyncSession, artist_id: int):
        query = select(Artists).options(
            joinedload(Artists.albums).load_only
            (Albums.id, Albums.album_name, Albums.album_cover)
        ).filter(Artists.id == artist_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_last_artist_album(db: AsyncSession, artist_id: int):
        query = select(Artists).options(
            joinedload(Artists.albums.and_(Albums.New == True)).load_only
            (Albums.id, Albums.album_name, Albums.album_cover)
        ).filter(Artists.id == artist_id)
        result = await db.execute(query)
        return result.scalars().first()
