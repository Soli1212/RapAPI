from fastapi import Depends, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.connection import get_db
from Application.Services import (PlaylistServices)
from Application.Auth import Authorize
from Application.Auth.RateLimiter import limiter
#schemas-----------------------------
from Domain.schemas.playlist import CreatePlaylist
from Domain.schemas.playlist import DeletePlaylist
from Domain.schemas.playlist import UpdatePlaylist
from Domain.schemas.playlist import AddMusic

@limiter.limit("5/minute")
async def create_playlist(PlaylistData: CreatePlaylist, request: Request, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await PlaylistServices.create_playlist(db, name = PlaylistData.name, user_id = authorize.get("id"), IsPublic=PlaylistData.IsPublic)

@limiter.limit("5/minute")
async def delete_playlist(request: Request, playlist_id: DeletePlaylist, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await PlaylistServices.delete_playlist(db, playlist_id.playlist_id, authorize.get("id"))

async def update_playlist(request: Request, PlaylistData: UpdatePlaylist, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await PlaylistServices.update_playlist(db, PlaylistData.playlist_id, authorize.get("id"), PlaylistData.name, PlaylistData.IsPublic)

@limiter.limit("10/minute")
async def add_music_to_playlist(request: Request, PlaylistData: AddMusic, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await PlaylistServices.add_music_to_playlist(db, PlaylistData.playlist_id, PlaylistData.music_id, authorize.get("id"))

async def delete_music_to_playlist(PlaylistData: AddMusic, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await PlaylistServices.delete_music_to_playlist(db, PlaylistData.playlist_id, PlaylistData.music_id, authorize.get("id"))

async def my_playlists(db: AsyncSession = Depends(get_db), authorize: Authorize = Depends()):
    return await PlaylistServices.my_playlists(db, authorize.get("id"))

async def get_my_playlist(db: AsyncSession = Depends(get_db), authorize: Authorize = Depends(), playlist_id: int = Path(gt=0), Page: int = Query(default=0, ge=0)):
    return await PlaylistServices.get_my_playlist(db = db, user_id = authorize.get("id"), playlist_id=playlist_id, offset=Page)

async def get_public_playlist(db: AsyncSession = Depends(get_db), playlist_id: int = Path(gt=0), Page: int = Query(default=0, ge=0)):
    return await PlaylistServices.get_public_playlist(db = db, playlist_id=playlist_id, offset=Page)