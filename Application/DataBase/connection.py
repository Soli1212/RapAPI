from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from .models.Base.base import Base
from dotenv import load_dotenv
from os import getenv

load_dotenv()
DATABASE_URL = getenv("DATABASE_URL")

engine = create_async_engine(
    url = DATABASE_URL
)
AsyncSessionLocal = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
