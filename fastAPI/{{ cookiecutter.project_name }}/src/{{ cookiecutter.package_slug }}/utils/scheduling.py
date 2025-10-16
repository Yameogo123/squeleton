
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def schedule_21h():
    pass


def add_jobs():
    scheduler.add_job(schedule_21h, "cron", hour=21, minute=0, id="job_21h", replace_existing=True)
