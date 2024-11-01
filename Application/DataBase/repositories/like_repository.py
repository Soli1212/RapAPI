from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
#-----------------------------------
from Application.DataBase.models import (Likes, Musics)


class LikeRepository:

    async def check_like_status(db: AsyncSession, music_id: int, user_id: int):
        query = select(Likes).filter(Likes.user_id == user_id, Likes.music_id == music_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def Like(db: AsyncSession, music_id: int, user_id: int):
        NewLike = Likes(user_id = user_id, music_id = music_id)
        db.add(NewLike)
        return True
    
    async def unlike(db: AsyncSession, LikeObject: check_like_status):
        await db.delete(LikeObject)
        return True

    async def get_likes_count(db: AsyncSession, music_id: int):
        query = select(func.count(Likes.id)).filter(
            Likes.music_id == music_id
        )
        result = await db.execute(query)
        return result.scalar_one()
    
    async def get_liked(db: AsyncSession, user_id: int, limit: int, offset: int):
        count_query = select(func.count(Likes.id)).filter(Likes.user_id == user_id)
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = (
            select(Musics.id, Musics.Music_name, Musics.Mucis_cover)
            .join(Likes, Musics.id == Likes.music_id)
            .filter(Likes.user_id == user_id)
            .offset(offset * limit)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.fetchall(), total_count