from pydantic import BaseModel
from pydantic import PositiveInt
class Like(BaseModel):
    music_id: PositiveInt
