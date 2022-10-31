import os
import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neectrally.settings')

app = celery.Celery('rallytascas')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))