from celery import Celery
from config.app_config import config


celery_app = Celery(
    "mailer",
    backend=config.celery_backend,
    broker=config.celery_broker
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True
)

celery_app.autodiscover_tasks(
    packages=["celery_tasks"],
    related_name="email_tasks",
)