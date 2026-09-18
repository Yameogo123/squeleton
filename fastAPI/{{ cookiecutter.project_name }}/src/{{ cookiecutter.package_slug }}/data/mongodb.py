from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from decouple import config
from fastapi import UploadFile
from loguru import logger
from fastapi_cache import FastAPICache
from bson.objectid import ObjectId

MONGODB_URL = config("MONGODB_URL")
DB_NAME = config("DB_NAME")

def get_database(): 
   client = AsyncIOMotorClient(MONGODB_URL)
   return client[DB_NAME]

dbname = get_database()
fs = AsyncIOMotorGridFSBucket(dbname) 
userdb = dbname["user"]

tables = {
    "user": userdb
}

async def init_indexes():
    await userdb.create_index("email", unique=True)
    await userdb.create_index("tel", unique=True)

actions = [
    "insert_one", "delete_one", "find_one", "update_one", "find_all",
    "purge", "insert_many", "update_many"
]

async def make_crud_action(tablename:str, action:str, **kwargs):
    if action not in actions or tablename not in tables.keys():
        raise ValueError(f"action must be one of: {actions} and table must be in {tables.keys()}")
    
    # Invalidate cache if mutating
    if action in ["insert_one", "delete_one", "update_one", "insert_many", "update_many", "purge"]:
        try:
            await FastAPICache.clear()
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    db_table = tables[tablename]
    fonctions = {
        "insert_one": db_table.insert_one, "find_one": db_table.find_one,
        "update_one": db_table.update_one, "delete_one": db_table.delete_one,
        "find_all": db_table.find, "purge": db_table.delete_many,
        "insert_many": db_table.insert_many, "update_many": db_table.update_many
    }
    
    if action == "find_all":
        cursor = fonctions[action](**kwargs)
        return await cursor.to_list(length=None)
    else:
        return await fonctions[action](**kwargs)

async def handle_file(action:str, file: UploadFile = None, file_content:bytes = b"", filename:str = "", id:str = ""):
    if action not in actions:
        raise ValueError(f"action must be one of: {actions}")

    try:
        if action == "insert_one":
            file_id = await fs.upload_from_stream(
                filename=file.filename,
                source=file_content,
                metadata={"content_type": file.content_type}
            )
            return str(file_id)

        elif action == "find_one":
            if filename:
                cursor = fs.find({"filename": filename})
                docs = await cursor.to_list(length=1)
                return docs[0] if docs else None
            else:
                if id:
                    cursor = fs.find({"_id": ObjectId(id)})
                    docs = await cursor.to_list(length=1)
                    return docs[0] if docs else None
                return None

        elif action == "delete_one":
            await fs.delete(ObjectId(id))
            return True
        
        return None
    except Exception as e:
        logger.error(e)
        return None