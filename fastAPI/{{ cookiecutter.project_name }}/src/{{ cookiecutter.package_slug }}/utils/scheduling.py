
from contextlib import asynccontextmanager
from fastapi import FastAPI
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from loguru import logger

# Configuration pour éviter les doublons
jobstores = {
    'default': MemoryJobStore()
}
job_defaults = {
    'coalesce': True,  # Combine les exécutions manquées en une seule
    'max_instances': 1,  # Une seule instance du job à la fois
    'misfire_grace_time': 15  # Grace period de 15 secondes
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
    
    yield
    
    # === SHUTDOWN ===
    try:
        scheduler.shutdown()
    except Exception:
        print("scheduler already killed")


