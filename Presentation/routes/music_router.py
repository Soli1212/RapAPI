from fastapi import APIRouter
from Presentation.controllers import music_controller

Router = APIRouter()

Router.get(
    path = "/p/{music_id}"
)(music_controller.get_music_by_id)

Router.get(
    path = "/popular"
)(music_controller.get_popular_musics)

Router.get(
    path = "/suggested"
)(music_controller.get_suggested_musics)