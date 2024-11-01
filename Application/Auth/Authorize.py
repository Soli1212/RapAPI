from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
#-----------------------------
from .JwtHandler import JWT
from Application.DataBase.repositories import UserRepository
from Application.DataBase.repositories import TokenRepository
from Application.DataBase.connection import AsyncSessionLocal, get_db
#-----------------------------
from Domain.errors.authorize import AccessTokenNotExist
from Domain.errors.authorize import AccessTokenBlocked
from Domain.errors.authorize import UserNotFound


async def Authorize(request: Request, db:AsyncSession = Depends(get_db)):
    Token = request.cookies.get("AccessToken", None)
    #----------------------------
    if not Token : 
        raise AccessTokenNotExist
    
    if await TokenRepository.is_blocked(db, Token): 
        raise AccessTokenBlocked
    #----------------------------
    verify = JWT().Verify(token = Token)
    UserExists = await UserRepository.get_user_by_id(db, user_id = verify["id"])
    #----------------------------
    if not UserExists : 
        raise UserNotFound
    
    return verify
    
async def if_Authorize(request: Request):
    async with AsyncSessionLocal() as db:
        try:
            if X := await Authorize(request = request, db = db) : 
                return X
        except : 
            return False

    