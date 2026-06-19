from celery import Celery
from config import settings
from logging_config import setup_logging


setup_logging()


celery_app = Celery(
    "bookings",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
celery_app.autodiscover_tasks(["tasks"])
import tasks.booking_tasks
