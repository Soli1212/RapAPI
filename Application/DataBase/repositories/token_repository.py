from Application.DataBase.models import BlockedToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class TokenRepository:
    
    async def add_token(db: AsyncSession, token: str) -> bool:
        blocked_token = BlockedToken(token=token)     
        try:
            db.add(blocked_token)
            return True
        except :
            return False

    async def is_blocked(db: AsyncSession, token: str) -> bool:
        query = select(BlockedToken).filter(BlockedToken.token == token)
        result = await db.execute(query)
        return result.scalars().first()
