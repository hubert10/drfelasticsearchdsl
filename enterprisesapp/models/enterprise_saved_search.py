import datetime
import uuid
from django.db import models
from enterprisesapp.models.enterprise import Enterprise
from django.utils.translation import ugettext_lazy as _


class EnterpriseSavedSearch(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    enterprise_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = _("Enterprise Saved Search")
        verbose_name_plural = _("Enterprise Saved Searches")
