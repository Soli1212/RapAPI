from fastapi import APIRouter
from Presentation.controllers import artist_controller

Router = APIRouter()


Router.get(
    path = "/{artist_id}"
)(artist_controller.get_artist_details)

Router.get(
    path = "/generation/{generation}"
)(artist_controller.get_artists_by_generation)

Router.get(
    path = "/musics/{artist_id}"
)(artist_controller.get_artist_musics)

Router.get(
    path = "/popular/{artist_id}"
)(artist_controller.get_artist_popular_musics)

Router.get(
    path = "/suggested/{artist_id}"
)(artist_controller.get_artist_suggested_musics)

Router.get(
    path = "/albums/{artist_id}"
)(artist_controller.get_artist_albums)

Router.get(
    path = "/lastalbum/{artist_id}"
)(artist_controller.get_last_artist_album)

