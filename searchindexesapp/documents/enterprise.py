from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.fields import ListField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_5_0
from enterprisesapp.models.enterprise import Enterprise
from enterprisesapp.models.skill import Skill
from elasticsearch_dsl import analyzer

from searchindexesapp.analyzers import html_strip, custom_analyzer


__all__ = ("EntrepriseDocument",)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={"read_only_allow_delete": None},
    max_result_window=500000
)

@INDEX.doc_type
class EnterpriseDocument(Document):
    """Enterprise Elasticsearch document."""

    name = StringField(
        analyzer=custom_analyzer,
        fields={
            "raw": KeywordField(),
            "mlt": StringField(analyzer="english"),
            "suggest": fields.CompletionField(),
        },
    )

    description = StringField(
        analyzer=custom_analyzer,
        fields={
            "raw": KeywordField(),
            "mlt": StringField(analyzer="english"),
        },
    )

    summary = StringField(
        analyzer=custom_analyzer,
        fields={
            "raw": KeywordField(),
            "mlt": StringField(analyzer="english"),
        },
    )

    # Publication date
    created = fields.DateField()

    # Tags
    skills = StringField(attr="skills_indexing", multi=True)
    skills_en = StringField(attr="skills_en_indexing", multi=True)
    skills_fr = StringField(attr="skills_fr_indexing", multi=True)
    # Tags
    sectors = StringField(attr="sectors_indexing", multi=True)
    sectors_en = StringField(attr="sectors_en_indexing", multi=True)
    sectors_fr = StringField(attr="sectors_fr_indexing", multi=True)

    # class Index:
    #     name = 'dev_enterprise'
    #     # See Elasticsearch Indices API reference for available settings
    #     settings = {'max_result_window': 500000,}
    class Django(object):
        model = Enterprise  # The model associate with this Document

    class Meta(object):
        parallel_indexing = True
        queryset_pagination = 500  # This will split the queryset
        #                           # into parts while indexing

    def prepare_summary(self, instance):
        """Prepare summary."""
        return instance.summary[:32766] if instance.summary else None
