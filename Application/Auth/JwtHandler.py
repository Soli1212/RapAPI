from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from base64 import urlsafe_b64decode
from datetime import timedelta, datetime
from dotenv import load_dotenv
from os import getenv

# ----------------------
from Domain.errors.authorize import TokenHasExpired, InvalidToken

load_dotenv()
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")

class JWT:
    def __init__(self, algoritm: str = "HS256", expireTime: int = 50) -> None:
        self.secretKey = JWT_SECRET_KEY
        self.algoritm = algoritm
        self.expireTime = expireTime  # 50 days

    def Create(self, data: dict) -> str:
        ExpireTime = datetime.utcnow() + timedelta(days=self.expireTime)
        data["exp"] = ExpireTime
        token = encode(
            payload=data,
            key=self.secretKey,
            algorithm=self.algoritm
        )
        return token

    def Verify(self, token: str) -> bool:
        try:
            Decode = decode(
                jwt=token,
                key=self.secretKey,
                algorithms=self.algoritm
            )
            return Decode
        except ExpiredSignatureError:
            raise TokenHasExpired
        except InvalidTokenError:
            raise InvalidToken

    @staticmethod
    def get_exp_from_token(token: str):
        try:
            header, payload, signature = token.split('.')
            payload_decoded = urlsafe_b64decode(payload + '==')
            return eval(payload_decoded.decode()).get("exp", None)
        except Exception:
            return None
