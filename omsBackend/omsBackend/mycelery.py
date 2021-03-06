# -*- coding: utf-8 -*-
# author: huashaw

from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omsBackend.settings')
celery_app = Celery('omsBackend', result_backend='django-db')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
celery_app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'