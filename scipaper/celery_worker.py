from scipaper.config import settings
from celery import Celery

# Initialize Celery
celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["scipaper.tasks.analysis_tasks"]
)

celery_app.conf.update(
    task_track_started=True,
)
