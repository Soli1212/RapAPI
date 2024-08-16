from fastapi import HTTPException, status

class NoAlbumFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="No Album found !")
