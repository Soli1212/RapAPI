from fastapi import APIRouter
from Presentation.controllers import playlist_controller
Router = APIRouter()


Router.post(
    path = "/new",
)(playlist_controller.create_playlist)

Router.post(
    path = "/delete",
)(playlist_controller.delete_playlist)

Router.post(
    path = "/update",
)(playlist_controller.update_playlist)

Router.post(
    path = "/addmusic",
)(playlist_controller.add_music_to_playlist)

Router.post(
    path = "/deletemusic",
)(playlist_controller.delete_music_to_playlist)

Router.get(
    path = "/me/",
)(playlist_controller.my_playlists)
    
Router.get(
    path = "/get/{playlist_id}",
)(playlist_controller.get_my_playlist)

Router.get(
    path = "/public/{playlist_id}",
)(playlist_controller.get_public_playlist)



