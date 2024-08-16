from fastapi import APIRouter
from Presentation.controllers import user_controller
Router = APIRouter()




Router.get(
    path = "/login"
)(user_controller.login)

Router.get(
    path = "/auth"
)(user_controller.auth)

Router.get(
    path = "/me"
)(user_controller.me)

Router.get(
    path = "/logout"
)(user_controller.LogOut)

Router.get(
    path = "/view/{user_id}"
)(user_controller.user)

