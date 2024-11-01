from sqlalchemy.ext.asyncio import AsyncSession
#-----------------------------------
from Application.DataBase.repositories import LikeRepository, MusicRepository
#-errors----------------------------
from Domain.errors.like import LikeFailed

class LikeServices:
    
    @staticmethod
    async def check_like_status(db: AsyncSession, music_id: int, user_id: int):
        check = await LikeRepository.check_like_status(db, user_id = user_id, music_id = music_id)
        if check :
            return True
        else:
            return False
    
    @staticmethod
    async def do_like(db: AsyncSession, music_id: int, user_id: int):        
        like = await LikeRepository.check_like_status(db, user_id = user_id, music_id = music_id)
        if not like :
            if not await MusicRepository.get_short_music_data(db, music_id): 
                raise LikeFailed
            if await LikeRepository.Like(db, music_id, user_id):
                return {"message" : f"music {music_id} liked +"}
        else:
            if await LikeRepository.unlike(db, like):
                return {"message" : f"music {music_id} unliked -"}
        
    @staticmethod
    async def get_likes_count(db: AsyncSession, music_id: int):
        LikesCount = await LikeRepository.get_likes_count(db, music_id)
        if LikesCount:
            return LikesCount
        
    @staticmethod # - > change limit
    async def get_liked(db: AsyncSession, user_id: int, offset: int, limit: int = 1):
        musics, total_count = await LikeRepository.get_liked(db, user_id, limit, offset)
        if musics:
            return {
                "total_pages" : (total_count + limit - 1) // limit,
                "musics" : [{"id" : i.id ,"Music_name": i.Music_name, "Mucis_cover": i.Mucis_cover} for i in musics]
            }
        
            