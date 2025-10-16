
import json
#from decouple import config
from passlib.context import CryptContext
from fastapi import HTTPException
from loguru import logger
import httpx

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def from_model_to_dict(model):
    return json.loads(model.json())

def serialize_model(model:dict):
    try:
        if '_id' in model.keys():
            model["_id"] = str(model["_id"])
    except Exception as e:
        logger.error(f"error in serialize_model: {e}")
    return model

# Function to hash user password
def hash_pwd(pwd:str):
    return pwd_context.hash(pwd)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def http_error(e, status:int = 400):
    raise HTTPException(status_code=status, detail={"error": str(e)}) 


def send_push_notification(expo_token: str, title: str, body: str, data: dict = None):
    """
    Send push notification via Expo (synchronous version)
    """
    message = {
        "to": expo_token,
        "sound": "default",
        "title": title,
        "body": body,
        "data": data or {}
    }
    EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"
    with httpx.Client() as client:
        response = client.post(EXPO_PUSH_URL, json=message, data = message)
        return response.json()