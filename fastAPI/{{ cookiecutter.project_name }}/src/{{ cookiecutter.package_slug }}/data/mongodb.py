

from pymongo import MongoClient
from gridfs import GridFS
from decouple import config
from fastapi import UploadFile
from loguru import logger


MONGODB_URL = config("MONGODB_URL")
DB_NAME = config("DB_NAME")

def get_database(): 
   client = MongoClient(MONGODB_URL)
   return client[DB_NAME]

dbname = get_database()
fs = GridFS(dbname) 
userdb = dbname["user"]
roledb = dbname["role"]

userdb.create_index("email", unique=True)

tables = {
    "user": userdb
}

actions = [
    "insert_one", "delete_one", "find_one", "update_one", "find_all",
    "purge", "insert_many", "update_many"
]



def make_crud_action(tablename:str, action:str, **kwargs):
    if action not in actions or tablename not in tables.keys():
        raise ValueError(f"action must be one of: {actions} and table must be in {tables.keys()}")
    db_table = tables[tablename]
    fonctions = {
        "insert_one": db_table.insert_one, "find_one": db_table.find_one,
        "update_one": db_table.update_one, "delete_one": db_table.delete_one,
        "find_all": db_table.find, "purge": db_table.delete_many,
        "insert_many": db_table.insert_many, "update_many": db_table.update_many
    }
    return fonctions[action](**kwargs)


def handle_file(action:str, file: UploadFile = None, file_content:str = "", filename:str = "", id:str = ""):
    if action not in actions:
        raise ValueError(f"action must be one of: {actions}")

    try:
        if action == "insert_one":
            file_id = fs.put(file_content, filename=file.filename, content_type=file.content_type)
            return str(file_id)

        elif action == "find_one":
            if filename:
                return fs.find_one({"filename": filename})
            else:
                if id:
                    return fs.get(id)
                return None

        elif action == "delete_one":
            fs.delete(id)
            resp = dbname["fs.files"].delete_one({"_id": id})
            dbname["fs.chunks"].delete_many({"files_id": id})
            return resp
        
        return None
    except Exception as e:
        logger.error(e)
        return None