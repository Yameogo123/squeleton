"""Response cache (fastapi-cache2): Redis when REDIS_URL is set, in-memory otherwise.

Usage on a route:  @cache(expire=settings.CACHE_TTL, namespace="user")
Invalidate:        await invalidate("user")   (done automatically on every DB write of that table)

In-memory cache is per process: with WORKERS > 1 use Redis so invalidation reaches every worker.
"""

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
{% if cookiecutter.use_redis == 'yes' %}from fastapi_cache.backends.redis import RedisBackend
{% endif %}from loguru import logger
{% if cookiecutter.use_redis == 'yes' %}from redis import asyncio as aioredis
{% endif %}
from {{ cookiecutter.package_slug }}.core.config import settings

PREFIX = "{{ cookiecutter.package_slug }}-cache"


async def init_cache() -> None:
{%- if cookiecutter.use_redis == 'yes' %}
    if settings.REDIS_URL:
        redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=False)
        FastAPICache.init(RedisBackend(redis), prefix=PREFIX, expire=settings.CACHE_TTL)
        logger.info("Redis cache initialized")
        return
{%- endif %}
    FastAPICache.init(InMemoryBackend(), prefix=PREFIX, expire=settings.CACHE_TTL)
    logger.info("In-memory cache initialized")


async def invalidate(namespace: str | None = None) -> None:
    try:
        await FastAPICache.clear(namespace=namespace)
    except Exception as e:  # cache must never break a write
        logger.warning(f"Cache invalidation failed ({namespace}): {e}")
