from pydantic import BaseModel
from pydantic import PositiveInt
from typing import Optional
class CreatePlaylist(BaseModel):
    name: str
    IsPublic: Optional[bool] = False

class DeletePlaylist(BaseModel):
    playlist_id: int

class UpdatePlaylist(BaseModel):
    playlist_id: int
    name: Optional[str] = None
    IsPublic: Optional[bool] = None

class AddMusic(BaseModel):
    playlist_id: int
    music_id: int



