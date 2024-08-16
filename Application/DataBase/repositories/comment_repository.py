from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from Application.DataBase.models import Comments, Users

class CommentRepository:

    async def add_comment(db: AsyncSession, music_id: int, user_id: int, comment_text: str):
        new_comment = Comments(user_id=user_id, music_id=music_id, content=comment_text)
        db.add(new_comment)
        return True

    async def get_comments(db: AsyncSession, music_id: int, limit: int, offset: int):
        count_query = select(func.count(Comments.id)).filter(
            Comments.music_id == music_id
        )
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar_one()

        query = (
            select(Comments)
            .options(
                joinedload(Comments.user).load_only(Users.id, Users.name, Users.profile_pic)
            )
            .filter(Comments.music_id == music_id)
            .limit(limit)
            .offset(offset * limit)
        )
        result = await db.execute(query)
        comments = result.scalars().all()
        return comments, total_count
