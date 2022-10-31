import os
import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neectrally.settings')

app = celery.Celery('rallytascas')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()