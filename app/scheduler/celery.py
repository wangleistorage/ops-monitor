from celery import Celery

# Celery对象
celery_app = Celery('celery_app')

# 导入配置
celery_app.config_from_object('scheduler.celeryconfig')