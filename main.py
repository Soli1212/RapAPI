from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
#=================================
from Presentation.routes.user_routes import Router as UserRouters
from Presentation.routes.artist_router import Router as ArtistRouter
from Presentation.routes.album_router import Router as AlbumRouter
from Presentation.routes.music_router import Router as MusicRouter
from Presentation.routes.likes_router import Router as LikeRouter
from Presentation.routes.comment_router import Router as CommentRouter
from Presentation.routes.playlist_router import Router as PLaylistRouter
#=================================
from Application.Auth.RateLimiter import limiter
from Application.DataBase.connection import init_db
#=================================
from uvicorn import run

app = FastAPI()

# DataBase startup----------------------------------------
@app.on_event("startup")
async def on_startup():
    await init_db()
#--------------------------------------------------------

#Config Routers------------------------------------------
app.include_router(prefix = "/user", router = UserRouters, tags=["user"])
app.include_router(prefix = "/artists", router = ArtistRouter, tags=["artists"])
app.include_router(prefix = "/albums", router = AlbumRouter, tags=["albums"])
app.include_router(prefix = "/music", router = MusicRouter, tags=["music"])
app.include_router(prefix = "/like", router = LikeRouter, tags=["like"])
app.include_router(prefix = "/comment", router = CommentRouter, tags=["comment"])
app.include_router(prefix = "/playlist", router = PLaylistRouter, tags=["playlist"])
#---------------------------------------------------------

#Config RateLimiter---------------------------------------
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
#---------------------------------------------------------

# Cors middleware-----------------------------------------
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#---------------------------------------------------------
@app.get("/")
async def main():
    return "hi🙂"

if __name__ == "__main__":
    run(app=app, host="0.0.0.0", port=8000)