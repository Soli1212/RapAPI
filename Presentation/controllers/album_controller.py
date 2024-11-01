from fastapi import Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.connection import get_db
from Application.Services import (AlbumServices)



async def get_album(album_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await AlbumServices.get_album(db, album_id)

async def get_new_albums(db: AsyncSession = Depends(get_db), Page: int = Query(default = 0, ge = 0)):
    return await AlbumServices.get_new_albums(db = db, offset = Page)

async def get_suggested_albums(db: AsyncSession = Depends(get_db)):
    return await AlbumServices.get_suggested_albums(db = db)
