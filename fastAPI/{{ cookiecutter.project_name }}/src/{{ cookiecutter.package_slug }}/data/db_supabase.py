"""Supabase (Postgres + Storage) access with the async client.

Same interface as the MongoDB module: insert -> id(s) as str, find -> dict(s),
update/delete -> affected count (int). Rows expose their primary key as both `id` and `_id`
so entities/routers stay database agnostic. Create tables/indexes with SQL migrations.
"""

import inspect
import mimetypes
import re
import uuid
from typing import Any

from loguru import logger
from supabase import AsyncClient, acreate_client

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.utils.cache import invalidate

ID_FIELD = "id"
TABLES = {"user"}
ACTIONS = {"insert_one", "insert_many", "find_one", "find_all", "update_one", "update_many", "delete_one", "purge"}
WRITE_ACTIONS = ACTIONS - {"find_one", "find_all"}

_client: AsyncClient | None = None


async def connect() -> None:
    global _client
    _client = await acreate_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    logger.info("Supabase client ready")


async def disconnect() -> None:
    pass


def get_client() -> AsyncClient:
    if _client is None:
        raise RuntimeError("Database not connected: connect() must run in the app lifespan")
    return _client


async def ping() -> bool:
    try:
        await get_client().table("user").select("id").limit(1).execute()
        return True
    except Exception:
        return False


async def init_indexes() -> None:
    # Postgres: indexes/constraints live in SQL migrations (supabase/migrations)
    pass


def to_id(value: Any) -> str:
    return str(value)


def _row(row: dict | None) -> dict | None:
    if row and ID_FIELD in row:
        row["_id"] = str(row[ID_FIELD])
    return row


def _apply_filter(query, filter_: dict | None):
    for key, value in (filter_ or {}).items():
        query = query.eq(ID_FIELD if key == "_id" else key, value)
    return query


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
    if action in {"update_many", "purge"} and not filter:
        raise ValueError(f"{action} without filter is refused (would touch the whole table)")

    table = get_client().table(tablename)

    match action:
        case "insert_one":
            res = await table.insert(document).execute()
            result = str(res.data[0][ID_FIELD]) if res.data else None
        case "insert_many":
            res = await table.insert(documents).execute()
            result = [str(r[ID_FIELD]) for r in res.data]
        case "find_one":
            res = await _apply_filter(table.select("*"), filter).limit(1).execute()
            result = _row(res.data[0]) if res.data else None
        case "find_all":
            query = _apply_filter(table.select("*"), filter)
            if limit:
                query = query.range(skip, skip + limit - 1)
            res = await query.execute()
            result = [_row(r) for r in res.data]
        case "update_one" | "update_many":
            res = await _apply_filter(table.update(update), filter).execute()
            result = len(res.data)
        case "delete_one" | "purge":
            res = await _apply_filter(table.delete(), filter).execute()
            result = len(res.data)

    if action in WRITE_ACTIONS:
        await invalidate(tablename)
    return result


######### files (Supabase Storage)


def _bucket():
    return get_client().storage.from_(settings.SUPABASE_BUCKET_NAME)


def _safe_name(filename: str) -> str:
    # unique + no path traversal / weird chars in the object key
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", filename or "file")[-100:]
    return f"{uuid.uuid4().hex}_{stem}"


async def file_upload(filename: str, content: bytes, content_type: str) -> str:
    key = _safe_name(filename)
    await _bucket().upload(key, content, {"content-type": content_type})
    return key


async def file_read(file_id: str) -> tuple[bytes, str, str] | None:
    """Returns (content, filename, content_type) or None."""
    try:
        content = await _bucket().download(file_id)
    except Exception:
        return None
    content_type = mimetypes.guess_type(file_id)[0] or "application/octet-stream"
    return content, file_id.split("_", 1)[-1], content_type


async def file_public_url(file_id: str) -> str:
    url = _bucket().get_public_url(file_id)
    return await url if inspect.isawaitable(url) else url


async def file_delete(file_id: str) -> bool:
    try:
        await _bucket().remove([file_id])
        return True
    except Exception as e:
        logger.warning(f"Storage delete failed for {file_id}: {e}")
        return False
