from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='celery')

app.autodiscover_tasks()
