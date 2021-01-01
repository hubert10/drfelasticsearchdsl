from __future__ import absolute_import
from drfelasticsearchdsl.celery import app as celery_app

#  Then, to ensure that the Celery app is loaded when Django starts, you need to import this app in the __init__.py file.

__all__ = ["celery_app"]
