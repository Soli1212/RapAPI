from fastapi import APIRouter
from Presentation.controllers import like_controller


Router = APIRouter()

Router.post(
    path = "/check"
)(like_controller.check_like_status)


Router.post(
    path = "/do"
)(like_controller.do_like)


Router.post(
    path = "/count"
)(like_controller.get_likes_count)


Router.get(
    path = "/liked"
)(like_controller.get_liked)


