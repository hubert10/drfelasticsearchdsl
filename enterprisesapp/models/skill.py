import uuid
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from drfelasticsearchdsl.tasks import task_reindex_new_added_skill_in_background


class Skill(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self):
        return self.name


@receiver(post_save, sender=Skill)
def reindex_new_added_skill(sender, **kwargs):
    """
    django synchronous signal that helps at reindexing profile object from the index whenever an profile is created!
    """
    # Reindex saved profile with created, active and account_status equals to True
    if kwargs["created"]:
        task_reindex_new_added_skill_in_background.delay(kwargs["instance"].id)
