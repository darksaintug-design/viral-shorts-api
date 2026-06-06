from celery import Celery
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    'viral_shorts',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
)
