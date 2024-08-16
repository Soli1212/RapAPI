from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.repositories import CommentRepository, MusicRepository
from Domain.errors.comment import CommentFailed, NotCommentFound

class CommentServices:
    
    @staticmethod
    async def add_comment(db: AsyncSession, music_id: int, comment_text: str, user_id: int):
        if not await MusicRepository.get_short_music_data(db, music_id):
            raise CommentFailed
        success = await CommentRepository.add_comment(db, music_id, user_id, comment_text)
        if success:
            return True


    @staticmethod # - > change limit
    async def get_comments(db: AsyncSession, music_id: int, offset: int, limit: int = 1):
        if not await MusicRepository.get_short_music_data(db, music_id):
            raise CommentFailed
        comments, total_count = await CommentRepository.get_comments(db, music_id, limit, offset)
        if not comments:
            raise NotCommentFound
        return {
            "total_pages": (total_count + limit - 1) // limit,
            "comments": [
                {
                    "content": comment.content,
                    "user": comment.user
                }
                for comment in comments
            ]
        }
