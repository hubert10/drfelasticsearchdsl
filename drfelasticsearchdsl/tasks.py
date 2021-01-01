from __future__ import absolute_import
from celery import shared_task
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry


@shared_task
def task_reindex_new_added_enterprise_in_background(enterprise):
    from enterprisesapp.models.enterprise import Enterprise

    _instance = Enterprise.objects.get(id=enterprise)
    registry.update(_instance)
    return "Entreprise Successfully Indexed!"


@shared_task
def task_reindex_new_added_skill_in_background(skill):
    from enterprisesapp.models.skill import Skill

    _instance = Skill.objects.ger(id=skill)
    registry.update(_instance)
    return "Skill Successfully Indexed!"


@shared_task
def task_create_enterprise_saved_searches_in_background(enterprise, order):
    from enterprisesapp.models.enterprise_saved_search import EnterpriseSavedSearch

    EnterpriseSavedSearch.objects.create(enterprise_id=enterprise, order=order)
    return "Entreprise Saved Search Successfully Created!"
