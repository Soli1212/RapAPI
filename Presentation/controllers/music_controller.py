from fastapi import Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.connection import get_db
from Application.Services import (MusicServices)

async def get_music_by_id(music_id: int = Path(gt = 0), db: AsyncSession = Depends(get_db)):
    return await MusicServices.get_music_by_id(db, music_id)

async def get_popular_musics(db: AsyncSession = Depends(get_db), Page: int = Query(default=0, ge=0)):
    return await MusicServices.get_popular_musics(db, Page)
    
async def get_suggested_musics(db: AsyncSession = Depends(get_db), Page: int = Query(default=0, ge=0)):
    return await MusicServices.get_suggested_musics(db, Page)
    