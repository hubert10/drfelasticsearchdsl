from __future__ import absolute_import
import os
from celery import Celery
from celery.app.registry import TaskRegistry
from drfelasticsearchdsl.tasks import (
    task_reindex_new_added_enterprise_in_background,
    task_reindex_new_added_skill_in_background,
    task_create_enterprise_saved_searches_in_background,
)
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drfelasticsearchdsl.settings")


app = Celery("drfelasticsearchdsl")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object("django.conf:settings")

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

# This line will tell Celery to autodiscover all your tasks.py that are in your app foldersapp
registration = TaskRegistry()
registration.register(task_reindex_new_added_enterprise_in_background)
registration.register(task_reindex_new_added_skill_in_background)
registration.register(task_create_enterprise_saved_searches_in_background)
