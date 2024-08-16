from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
#-----------------------------------
from Application.DataBase.models import Users, Playlists

class UserRepository:

    async def get_user_by_email(db: AsyncSession, email: str):
        try:
            query = select(Users).filter(Users.email == email)
            result = await db.execute(query)
            return result.scalars().first()
        except NoResultFound:
            return None

    async def get_user_by_id(db: AsyncSession, user_id: int):
        try:
            query = select(Users).filter(Users.id == user_id)
            result = await db.execute(query)
            return result.scalars().first()
        except NoResultFound:
            return None

    async def get_me(db: AsyncSession, user_id: int):
        try:
            query = select(Users).options(
                joinedload(Users.playlists).load_only(Playlists.id, Playlists.name, Playlists.IsPublic)
            ).filter(Users.id == user_id)
            result = await db.execute(query)
            user = result.scalars().first()
            return user
        except NoResultFound:
            return None

    async def create_user(db: AsyncSession, user: Users):
        try:
            db.add(user)
            await db.flush()
            return user.id
        except:
            return None

    async def get_user(db: AsyncSession, user_id: int):
        try:
            query = select(Users).options(
                joinedload(Users.playlists.and_(Playlists.IsPublic == True)).load_only(Playlists.id, Playlists.name, Playlists.IsPublic)
            ).filter(Users.id == user_id)
            result = await db.execute(query)
            user = result.scalars().first()
            if user:
                return user
            else:
                return None
        except NoResultFound:
            return None
