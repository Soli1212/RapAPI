from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from httpx import AsyncClient
from dotenv import load_dotenv
from os import getenv
# Auth--------------------------
from Application.Auth import (JWT)
#------------------------------
from Application.DataBase.models import Users
from Application.DataBase.repositories import UserRepository
from Application.DataBase.repositories import TokenRepository
# errors------------------------
from Domain.errors.user import (
    UserNotFound, ExpNotFound, NoCodeProvided, UnknowError
)
from Domain.errors.authorize import (
    AccessTokenNotExist
)


load_dotenv()

class UserServices:

    @staticmethod
    def login():
        google_auth_url = getenv("google_auth_url")
        return RedirectResponse(google_auth_url)
    

    @staticmethod
    async def auth(db: AsyncSession, response: Response, query_params: dict):
        code = query_params.get('code')
        if not code:
            raise NoCodeProvided

        token_url = getenv("token_url")
        token_data = {
            "code": code,
            "client_id": getenv("client_id"),
            "client_secret": getenv("client_secret"),
            "redirect_uri": getenv("REDIRECT_URI"),
            "grant_type": "authorization_code",
        }

        async with AsyncClient() as client:
            token_response = await client.post(token_url, json=token_data)
            token_json = token_response.json()
            if 'error' in token_json:
                raise UnknowError(error=token_json["error"])

            access_token = token_json.get('access_token')
            user_info_url = getenv("user_info_url")
            user_info_params = {"access_token": access_token}
            user_info_response = await client.get(user_info_url, params=user_info_params)

        user_info_json = user_info_response.json()
        cookies_exp = (datetime.utcnow() + timedelta(days=50)).strftime("%a, %d-%b-%Y %H:%M:%S GMT")

        if user := await UserRepository.get_user_by_email(db, user_info_json.get("email")):
            response.set_cookie(
                key="AccessToken",
                value=JWT().Create(data={"id": user.id}),
                httponly=True,
                secure=True,
                expires=cookies_exp
            )
            return {"message": "You have successfully logged in"}

        NewUser = Users(
            email=user_info_json.get("email"),
            name=user_info_json.get("name"),
            profile_pic=user_info_json.get("picture"),
        )

        if user := await UserRepository.create_user(db, NewUser):
            response.set_cookie(
                key="AccessToken",
                value=JWT().Create(data={"id": user}),
                httponly=True,
                secure=True,
                expires=cookies_exp
            )
            return {"message": "You have successfully logged in"}


    @staticmethod
    async def get_me(db: AsyncSession, user_id: int):
        "Requires login and authentication"
        return await UserRepository.get_me(db, user_id)


    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        "No need to depend"

        user = await UserRepository.get_user(db, user_id)
        if user:
            return {
                "name": user.name,
                "profile_pic": user.profile_pic,
                "Playlists": [{"id": playlist.id, "name": playlist.name} for playlist in user.playlists]
            }
        else:
            raise UserNotFound


    @staticmethod
    async def log_out(db: AsyncSession, response: Response, request: Request):
        """Sign out and block the JWT token if it is valid."""
        
        token = request.cookies.get("AccessToken", None)
        if token:
            exp_timestamp = JWT.get_exp_from_token(token=token)
            if exp_timestamp:
                exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
                current_datetime = datetime.utcnow()
                if current_datetime < exp_datetime:
                    if not await TokenRepository.is_blocked(db, token):
                        await TokenRepository.add_token(db, token)
                response.delete_cookie(key="AccessToken")
                return {"message": "Logout successful"}
            else:
                raise ExpNotFound
        else:
            raise AccessTokenNotExist
