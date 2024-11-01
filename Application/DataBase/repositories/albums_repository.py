from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from Application.DataBase.models import Albums, Artists, Musics

class AlbumRepository:

    async def get_album(db: AsyncSession, album_id: int):
        query = select(Albums).options(
            joinedload(Albums.artists).load_only(Artists.id, Artists.art_name, Artists.profile_pic),
            joinedload(Albums.musics).load_only(Musics.id, Musics.Music_name, Musics.Mucis_cover)
        ).filter(Albums.id == album_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_new_albums(db: AsyncSession, limit: int, offset: int):
        count_query = select(func.count(Albums.id)).filter(Albums.New == True)
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = select(Albums.id, Albums.album_name, Albums.album_cover).filter(
            Albums.New == True
        ).limit(limit).offset(offset * limit)
        result = await db.execute(query)
        return result.fetchall(), total_count

    async def get_suggested_albums(db: AsyncSession):
        query = select(Albums.id, Albums.album_name, Albums.album_cover).filter(Albums.Suggested == True)
        result = await db.execute(query)
        return result.fetchall()
