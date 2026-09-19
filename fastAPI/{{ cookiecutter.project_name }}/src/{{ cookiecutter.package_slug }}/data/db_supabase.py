from supabase import create_client, Client
from decouple import config
from fastapi import UploadFile
from loguru import logger
import os

SUPABASE_URL = config("SUPABASE_URL")
SUPABASE_KEY = config("SUPABASE_KEY")
SUPABASE_BUCKET_NAME = config("SUPABASE_BUCKET_NAME", default="uploads")

# Avoid fastAPI cache error if redis is not used
try:
    from fastapi_cache import FastAPICache
except ImportError:
    FastAPICache = None

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

actions = [
    "insert_one", "delete_one", "find_one", "update_one", "find_all",
    "purge", "insert_many", "update_many"
]

async def init_indexes():
    # Supabase uses Postgres. Indexes should be created via SQL migrations directly in the Supabase dashboard.
    pass

async def make_crud_action(tablename: str, action: str, **kwargs):
    if action not in actions:
        raise ValueError(f"action must be one of: {actions}")
    
    # Invalidate cache if mutating
    if action in ["insert_one", "delete_one", "update_one", "insert_many", "update_many", "purge"]:
        try:
            if FastAPICache is not None:
                await FastAPICache.clear()
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    try:
        if action == "insert_one":
            data = kwargs.get("document", {})
            res = supabase.table(tablename).insert(data).execute()
            return res.data[0] if res.data else None
            
        elif action == "insert_many":
            data = kwargs.get("documents", [])
            res = supabase.table(tablename).insert(data).execute()
            return res.data
            
        elif action == "find_one":
            filter_ = kwargs.get("filter", {})
            query = supabase.table(tablename).select("*")
            for k, v in filter_.items():
                query = query.eq(k, v)
            res = query.limit(1).execute()
            return res.data[0] if res.data else None
            
        elif action == "find_all":
            filter_ = kwargs.get("filter", {})
            query = supabase.table(tablename).select("*")
            for k, v in filter_.items():
                query = query.eq(k, v)
            res = query.execute()
            return res.data
            
        elif action == "update_one":
            filter_ = kwargs.get("filter", {})
            update_data = kwargs.get("update", {})
            
            # Simplified for generic update object mapping
            query = supabase.table(tablename).update(update_data)
            for k, v in filter_.items():
                query = query.eq(k, v)
            res = query.execute()
            return res.data[0] if res.data else None
            
        elif action == "update_many":
            filter_ = kwargs.get("filter", {})
            update_data = kwargs.get("update", {})
            
            query = supabase.table(tablename).update(update_data)
            for k, v in filter_.items():
                query = query.eq(k, v)
            res = query.execute()
            return res.data
            
        elif action == "delete_one" or action == "purge":
            filter_ = kwargs.get("filter", {})
            query = supabase.table(tablename).delete()
            for k, v in filter_.items():
                query = query.eq(k, v)
            res = query.execute()
            return True
    except Exception as e:
        logger.error(f"Supabase CRUD Error: {e}")
        return None


async def handle_file(action:str, file: UploadFile = None, file_content:bytes = b"", filename:str = "", id:str = ""):
    if action not in actions:
        raise ValueError(f"action must be one of: {actions}")

    try:
        if action == "insert_one":
            res = supabase.storage.from_(SUPABASE_BUCKET_NAME).upload(
                file.filename,
                file_content,
                {"content-type": file.content_type}
            )
            return file.filename  # We return filename as id for supabase storage

        elif action == "find_one":
            target_name = filename or id
            if target_name:
                # Return the public URL for the file
                res = supabase.storage.from_(SUPABASE_BUCKET_NAME).get_public_url(target_name)
                return {"filename": target_name, "url": res}
            return None

        elif action == "delete_one":
            target_name = filename or id
            if target_name:
                supabase.storage.from_(SUPABASE_BUCKET_NAME).remove([target_name])
                return True
        
        return None
    except Exception as e:
        logger.error(f"Supabase Storage Error: {e}")
        return None
