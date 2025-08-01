from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "interview_express",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"]
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分钟
    task_soft_time_limit=25 * 60,  # 25分钟
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
) 