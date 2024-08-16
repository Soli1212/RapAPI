from fastapi import APIRouter
from Presentation.controllers import album_controller

Router = APIRouter()

Router.get(
    path = "/details/{album_id}"
)(album_controller.get_album)

Router.get(
    path = "/news"
)(album_controller.get_new_albums)

Router.get(
    path = "/suggested"
)(album_controller.get_suggested_albums)