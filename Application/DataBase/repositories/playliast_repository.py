from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from Application.DataBase.models import Playlists, Musics, Users
from Application.DataBase.models.playlists import playlist_music_association

class PlaylistRepository:

    async def count_user_playlists(db: AsyncSession, user_id: int):
        query = select(func.count(Playlists.id)).filter(Playlists.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one()
    
    async def create_playlist(db: AsyncSession, name: str, user_id: int, IsPublic: bool):
        NewPlaylist = Playlists(name = name, user_id = user_id, IsPublic = IsPublic)
        db.add(NewPlaylist)
        return True
    
    async def Get_playlist_with_access(db: AsyncSession, user_id: int, playlist_id: int):
        query = select(Playlists).filter(Playlists.id == playlist_id, Playlists.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def delete_playlist(db: AsyncSession, playlist: Get_playlist_with_access):
        await db.delete(playlist)
        return True

    async def check_exist_music_in_playlist(db: AsyncSession, playlist_id: int, music_id: int):
        query = select(1).where(
            playlist_music_association.c.playlist_id == playlist_id,
            playlist_music_association.c.music_id == music_id,
        )
        result = await db.execute(query)
        return result.scalar() is not None

    async def add_music_to_playlist(db: AsyncSession, playlist_id: int, music_id: int):
        query = insert(playlist_music_association).values(playlist_id = playlist_id, music_id = music_id)
        await db.execute(query)
        return True

    async def delete_music_to_playlist(db: AsyncSession, playlist_id: int, music_id: int):
        query = delete(playlist_music_association).where(
            playlist_music_association.c.playlist_id == playlist_id,
            playlist_music_association.c.music_id == music_id
        )
        await db.execute(query)
        return True
    
    async def check_IsPublic(db: AsyncSession, playlist_id: int):
        query = select(Playlists).options(
            joinedload(Playlists.users).load_only(Users.id, Users.name, Users.profile_pic)
        ).filter(Playlists.id == playlist_id, Playlists.IsPublic == True)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def my_playlists(db: AsyncSession, user_id: int):
        query = select(Playlists.id, Playlists.name).filter(
            Playlists.user_id == user_id
        )
        result = await db.execute(query)
        return result.fetchmany()
    
    async def get_playlist(db: AsyncSession, playlist_id: int, limit: int, offset: int):
        count_query = select(func.count(playlist_music_association.c.music_id)).where(
            playlist_music_association.c.playlist_id == playlist_id
        )
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        subquery_stmt = (
            select(playlist_music_association.c.music_id)
            .filter(playlist_music_association.c.playlist_id == playlist_id)
            .limit(limit)
            .offset(offset * limit)
            .subquery()
        )
        result = await db.execute(
            select(Musics.id, Musics.Music_name, Musics.Mucis_cover)
            .filter(Musics.id.in_(subquery_stmt))
        )
        musics = result.all()
        return musics, total_count
    

