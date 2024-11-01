from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from Application.DataBase.models import Musics, Artists, Albums

class MusicRepository:
    async def get_short_music_data(db: AsyncSession, music_id: int):
        query = select(Musics.id, Musics.Music_name, Musics.Music_Content).filter(Musics.id == music_id)
        result = await db.execute(query)
        return result.fetchone()

    async def get_music_by_id(db: AsyncSession, music_id: int):
        query = select(Musics).options(
            joinedload(Musics.artists).load_only(Artists.id, Artists.art_name, Artists.profile_pic),
            joinedload(Musics.albums).load_only(Albums.id, Albums.album_name, Albums.album_cover)
        ).filter(Musics.id == music_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_popular_musics(db: AsyncSession, limit: int, offset: int):
        count_query = select(func.count(Musics.id)).filter(Musics.popular == True)
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = select(Musics.id, Musics.Music_name, Musics.Mucis_cover).filter(
            Musics.popular == True
        ).limit(limit).offset(limit * offset)
        result = await db.execute(query)

        return result.fetchall(), total_count
    
    async def get_suggested_musics(db: AsyncSession, limit: int, offset: int):
        count_query = select(func.count(Musics.id)).filter(Musics.Suggested == True)
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = select(Musics.id, Musics.Music_name, Musics.Mucis_cover).filter(
            Musics.Suggested == True
        ).limit(limit).offset(limit * offset)
        result = await db.execute(query)

        return result.fetchall(), total_count
