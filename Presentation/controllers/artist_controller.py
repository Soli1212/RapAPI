from fastapi import Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.connection import get_db
from Application.Services import (ArtistServices)

async def get_artist_musics(artist_id: int = Path(gt=0), Page:int = Query(default=0, ge=0), db: AsyncSession = Depends(get_db)):
    return await ArtistServices.get_artist_musics(db, artist_id, Page)


async def get_artist_details(artist_id: int = Path(gt=0), db:AsyncSession = Depends(get_db)):
    return await ArtistServices.get_artist_details(db, artist_id)


async def get_artists_by_generation(generation: int = Path(gt=0), db:AsyncSession = Depends(get_db), Page: int = Query(default=0, ge=0)):
    return await ArtistServices.get_artists_by_generation(db, generation, Page)


async def get_artist_popular_musics(artist_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await ArtistServices.get_artist_popular_musics(db, artist_id)


async def get_artist_suggested_musics(artist_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await ArtistServices.get_artist_suggested_musics(db, artist_id)


async def get_artist_albums(artist_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await ArtistServices.get_artist_albums(db, artist_id)


async def get_last_artist_album(artist_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    return await ArtistServices.get_last_artist_album(db, artist_id)