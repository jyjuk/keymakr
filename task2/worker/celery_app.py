import os

from celery import Celery

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["worker.tasks"],
)

celery_app.conf.beat_schedule = {
    "fetch-users-every-60-seconds": {
        "task": "worker.tasks.fetch_and_save_users",
        "schedule": 60.0,
    },
}

celery_app.conf.timezone = "UTC"
