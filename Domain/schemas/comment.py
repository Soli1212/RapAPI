from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, PositiveInt, validator


app = FastAPI()

class comment(BaseModel):
    music_id: PositiveInt
    comment_text: str

    @validator('comment_text')
    def validate_comment_text(cls, v):
        if len(v) > 500 or len(v) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment must have at least one and maximum 500 characters"
            )
        return v
