"""MongoDB access with the official PyMongo async driver (motor is deprecated).

CRUD results are normalized so routers/entities don't depend on the driver:
insert -> id(s) as str, find -> dict(s), update/delete -> affected count (int).
"""

from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from gridfs import AsyncGridFSBucket
from loguru import logger
from pymongo import AsyncMongoClient

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.utils.cache import invalidate

ID_FIELD = "_id"
TABLES = {"user"}
ACTIONS = {"insert_one", "insert_many", "find_one", "find_all", "update_one", "update_many", "delete_one", "purge"}
WRITE_ACTIONS = ACTIONS - {"find_one", "find_all"}

_client: AsyncMongoClient | None = None


async def connect() -> None:
    global _client
    _client = AsyncMongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000, tz_aware=True)
    await init_indexes()
    logger.info("MongoDB connected")


async def disconnect() -> None:
    if _client is not None:
        await _client.close()


def get_db():
    if _client is None:
        raise RuntimeError("Database not connected: connect() must run in the app lifespan")
    return _client[settings.DB_NAME]


async def ping() -> bool:
    try:
        await get_db().command("ping")
        return True
    except Exception:
        return False


async def init_indexes() -> None:
    users = get_db()["user"]
    await users.create_index("email_hash", unique=True, partialFilterExpression={"email_hash": {"$type": "string"}})
    await users.create_index("tel", unique=True, partialFilterExpression={"tel": {"$type": "string", "$gt": ""}})


def to_id(value: Any) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    try:
        return ObjectId(str(value))
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid id") from None


def _normalize_filter(filter_: dict | None) -> dict:
    filter_ = dict(filter_ or {})
    if ID_FIELD in filter_ and not isinstance(filter_[ID_FIELD], (ObjectId, dict)):
        filter_[ID_FIELD] = to_id(filter_[ID_FIELD])
    return filter_


async def make_crud_action(
    tablename: str,
    action: str,
    *,
    document: dict | None = None,
    documents: list[dict] | None = None,
    filter: dict | None = None,
    update: dict | None = None,
    limit: int = 0,
    skip: int = 0,
):
    if action not in ACTIONS or tablename not in TABLES:
        raise ValueError(f"action must be one of {sorted(ACTIONS)} and table one of {sorted(TABLES)}")

    table = get_db()[tablename]
    filter_ = _normalize_filter(filter)

    match action:
        case "insert_one":
            result = str((await table.insert_one(document)).inserted_id)
        case "insert_many":
            result = [str(i) for i in (await table.insert_many(documents)).inserted_ids]
        case "find_one":
            result = await table.find_one(filter_)
        case "find_all":
            result = await table.find(filter_).skip(skip).limit(limit).to_list(length=None)
        case "update_one":
            result = (await table.update_one(filter_, update)).modified_count
        case "update_many":
            result = (await table.update_many(filter_, update)).modified_count
        case "delete_one":
            result = (await table.delete_one(filter_)).deleted_count
        case "purge":
            result = (await table.delete_many(filter_)).deleted_count

    if action in WRITE_ACTIONS:
        await invalidate(tablename)
    return result


######### files (GridFS)


def _bucket() -> AsyncGridFSBucket:
    return AsyncGridFSBucket(get_db())


async def file_upload(filename: str, content: bytes, content_type: str) -> str:
    file_id = await _bucket().upload_from_stream(filename, content, metadata={"content_type": content_type})
    return str(file_id)


async def file_read(file_id: str) -> tuple[bytes, str, str] | None:
    """Returns (content, filename, content_type) or None."""
    try:
        grid_out = await _bucket().open_download_stream(to_id(file_id))
    except Exception:
        return None
    content = await grid_out.read()
    content_type = (grid_out.metadata or {}).get("content_type", "application/octet-stream")
    return content, grid_out.filename, content_type


async def file_delete(file_id: str) -> bool:
    try:
        await _bucket().delete(to_id(file_id))
        return True
    except Exception as e:
        logger.warning(f"GridFS delete failed for {file_id}: {e}")
        return False
