from fastapi import APIRouter
from Presentation.controllers import comment_controller

Router = APIRouter()


Router.post(
    path = "/add"
)(comment_controller.add_comment)

Router.get(
    path = "/get/{music_id}"
)(comment_controller.get_comments)

