from fastapi import HTTPException, status

class PlaylistLimit(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Playlist creation limit is over !")

class PlaylistNotExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="playlist not existas !")

class AvailableMusic(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Music is available in the playlist !")
        
class NotAvailableMusic(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Music is not available in the playlist !")
