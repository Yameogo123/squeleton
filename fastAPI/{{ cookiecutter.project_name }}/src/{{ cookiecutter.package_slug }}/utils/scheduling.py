
from contextlib import asynccontextmanager
from fastapi import FastAPI
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from loguru import logger
from decouple import config
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from redis import asyncio as aioredis
from {{ cookiecutter.package_slug }}.data.mongodb import init_indexes


# Configuration pour éviter les doublons
jobstores = {
    'default': MemoryJobStore()
}
job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 15
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    job_defaults=job_defaults
)


def schedule_21h():
    pass


def add_jobs():
    scheduler.add_job(schedule_21h, "cron", hour=21, minute=0, id="job_21h", replace_existing=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    name = multiprocessing.current_process().name
    if name == "SpawnProcess-1":
        if not scheduler.running:
            add_jobs()
            scheduler.start()
            logger.info("✅ Scheduler started in main process")
    else:
        logger.info(f"The name is not SpawnProcess-1 but {name}")
    
    REDIS_URL = config("REDIS_URL", default=None)
    if REDIS_URL:
        redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=False)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        logger.info("✅ Redis Cache initialized")
    else:
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
        logger.info("✅ InMemory Cache initialized")
    
    await init_indexes()
    
    yield
    
    # === SHUTDOWN ===
    try:
        scheduler.shutdown()
    except Exception:
        print("scheduler already killed")


