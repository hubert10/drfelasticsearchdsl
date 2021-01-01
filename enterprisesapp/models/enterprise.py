import uuid
import os
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# from drfelasticsearchdsl.tasks import task_reindex_enterprise_background
from django.db.models.signals import post_save, post_delete


class Enterprise(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField(
        "Skill", related_name="enterprise_skills", blank=True
    )
    sectors = models.ManyToManyField(
        "Sector", related_name="enterprise_sectors", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Enterprise")
        verbose_name_plural = _("Enterprises")

    def __str__(self):
        return self.name

    @property
    def skills_indexing(self):
        return [skill.name for skill in self.skills.all()]

    @property
    def skills_en_indexing(self):
        return [skill.name_en for skill in self.skills.all()]

    @property
    def skills_fr_indexing(self):
        return [skill.name_fr for skill in self.skills.all()]

    @property
    def sectors_indexing(self):
        return [sector.name for sector in self.sectors.all()]

    @property
    def sectors_en_indexing(self):
        return [sector.name_en for sector in self.sectors.all()]

    @property
    def sectors_fr_indexing(self):
        return [sector.name_fr for sector in self.sectors.all()]


# @receiver(post_save, sender=Enterprise)
# def index_new_added_enterprise(sender, **kwargs):

#     if kwargs["created"]:
#         task_enterprise_background.delay(kwargs["instance"].id)
