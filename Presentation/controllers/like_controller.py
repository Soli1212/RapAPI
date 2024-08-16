from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
#-------------------------------------------------
from Application.DataBase.connection import get_db
from Application.Services import (LikeServices)
from Application.Auth import Authorize
from Application.Auth.RateLimiter import limiter
#-------------------------------------------------
from Domain.schemas.like import Like

async def check_like_status(music_id: Like, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await LikeServices.check_like_status(db, music_id.music_id, authorize.get("id"))

@limiter.limit("7/minute")
async def do_like(music_id: Like, request: Request, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await LikeServices.do_like(db, music_id.music_id, authorize.get("id"))

async def get_likes_count(music_id: Like, db: AsyncSession = Depends(get_db)):
    return await LikeServices.get_likes_count(db, music_id.music_id)

async def get_liked(Page: int = Query(default=0, ge = 0), authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await LikeServices.get_liked(db, authorize.get("id"), Page)