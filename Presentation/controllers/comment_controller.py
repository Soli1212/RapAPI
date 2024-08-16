from fastapi import Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
#---------------------------------------------
from Application.DataBase.connection import get_db
from Application.Services import (CommentServices)
from Application.Auth import Authorize
from Application.Auth.RateLimiter import limiter
#---------------------------------------------
from Domain.schemas.comment import comment as CommentSchemas

@limiter.limit("2/minute")
async def add_comment(CommentData: CommentSchemas, request: Request, authorize: Authorize = Depends(), db: AsyncSession = Depends(get_db)):
    return await CommentServices.add_comment(db, music_id = CommentData.music_id, comment_text = CommentData.comment_text, user_id = authorize.get("id"))

async def get_comments(music_id: int, db: AsyncSession = Depends(get_db), Page: int = Query(default=0, ge=0)):
    return await CommentServices.get_comments(db, music_id, Page)