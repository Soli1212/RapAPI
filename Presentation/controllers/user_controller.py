from fastapi import Depends, Path
from fastapi import (Request, Response)
from fastapi.responses import RedirectResponse
#--------------------------------------
from sqlalchemy.ext.asyncio import AsyncSession
from Application.DataBase.connection import get_db
#--------------------------------------
from Application.Services.user_service import UserServices
from Application.Auth import (Authorize, if_Authorize)
from Application.Auth.RateLimiter import limiter

async def login():
    return UserServices.login()

async def auth(request: Request, response: Response, db:AsyncSession = Depends(get_db)):
    return await UserServices.auth(db, response, request.query_params)

async def me(db:AsyncSession = Depends(get_db), authorize: Authorize = Depends()):
    return await UserServices.get_me(db, authorize.get("id"))

async def user(request: Request, user_id: int = Path(gt = 0), db: AsyncSession = Depends(get_db)):
    if X := await if_Authorize(request = request) : 
        if X.get("id") == user_id : return RedirectResponse(url="/user/me")
    return await UserServices.get_user(db, user_id)

@limiter.limit("5/minute")
async def LogOut(response: Response, request: Request, db:AsyncSession = Depends(get_db)):
    return await UserServices.log_out(db, response=response, request=request)