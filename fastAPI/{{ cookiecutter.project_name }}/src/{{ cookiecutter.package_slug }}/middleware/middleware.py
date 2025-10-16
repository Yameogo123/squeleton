
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
import jwt
from decouple import config


JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")
EXPIRY = int(config("ACCESS_TOKEN_EXPIRE_MINUTES")) * 60


def token_response(access_token:str):
    return {"access_token": access_token, "token_type": "Bearer"}

def signJWT(userID:str):
    payload = {
        "userID": userID,
        "expiry": time.time() + EXPIRY
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token:str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expiry"] >= time.time() else None
    except Exception:
        return None
 

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization credentials")

    def verify_jwt(self, jwttoken: str) -> bool:
        payload = decodeJWT(jwttoken)
        return payload is not None