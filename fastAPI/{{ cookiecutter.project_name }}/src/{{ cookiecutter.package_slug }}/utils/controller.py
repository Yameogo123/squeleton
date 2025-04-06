
import json
#from decouple import config
from passlib.context import CryptContext
from fastapi import HTTPException
from loguru import logger

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


