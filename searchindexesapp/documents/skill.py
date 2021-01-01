from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from enterprisesapp.models.skill import Skill
from elasticsearch_dsl import analyzer
from searchindexesapp.analyzers import html_strip, custom_analyzer


__all__ = ("SkillDocument",)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={"read_only_allow_delete": False},
    # read_only_allow_delete=False
)


@INDEX.doc_type
class SkillDocument(Document):
    """Skill Elasticsearch document."""

    id = StringField(
        attr="id",
        analyzer=html_strip,
    )

    name = StringField(
        fields={
            "raw": KeywordField(),
            "suggest": fields.CompletionField(),
        },
    )
    # Date created
    created = fields.DateField()

    class Django(object):
        model = Skill  # The model associate with this Document

    class Meta(object):
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing
