"""Background jobs (APScheduler) + the app lifespan (startup/shutdown).

The scheduler runs inside the event loop (AsyncIOScheduler). When the API runs with
several workers/replicas, set SCHEDULER_ENABLED=true on ONE of them only,
otherwise every job runs N times.
"""

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from loguru import logger

from {{ cookiecutter.package_slug }}.core.config import settings
from {{ cookiecutter.package_slug }}.data import database
from {{ cookiecutter.package_slug }}.utils.cache import init_cache
{% if cookiecutter.use_redis == 'yes' %}

def _jobstores() -> dict:
    if not settings.REDIS_URL:
        return {}
    from urllib.parse import urlparse

    from apscheduler.jobstores.redis import RedisJobStore

    url = urlparse(settings.REDIS_URL)
    return {
        "default": RedisJobStore(
            jobs_key="apscheduler.jobs",
            run_times_key="apscheduler.run_times",
            host=url.hostname or "localhost",
            port=url.port or 6379,
            password=url.password,
            db=int(url.path.lstrip("/") or 0),
        )
    }
{% else %}

def _jobstores() -> dict:
    return {}  # default in-memory store
{% endif %}

scheduler = AsyncIOScheduler(
    jobstores=_jobstores(),
    job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 15},
)


async def schedule_21h():
    logger.info("21h job")


def add_jobs():
    scheduler.add_job(schedule_21h, "cron", hour=21, minute=0, id="job_21h", replace_existing=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    await init_cache()
    await database.connect()
    if settings.SCHEDULER_ENABLED and not scheduler.running:
        add_jobs()
        scheduler.start()
        logger.info("Scheduler started")

    yield

    # === SHUTDOWN ===
    if scheduler.running:
        scheduler.shutdown(wait=False)
    await database.disconnect()
    logger.info("Shutdown complete")
