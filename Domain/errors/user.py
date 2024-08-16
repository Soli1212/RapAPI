from fastapi import HTTPException, status



class NoCodeProvided(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="No code provided !")

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found !")

class ExpNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Expire time not Found !")

class UnknowError(HTTPException):
    def __init__(self, error):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail = error)
