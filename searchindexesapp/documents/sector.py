from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl_drf.analyzers import edge_ngram_completion
from django_elasticsearch_dsl_drf.versions import ELASTICSEARCH_GTE_5_0
from enterprisesapp.models.sector import Sector
from elasticsearch_dsl import analyzer


__all__ = ("SectorDocument",)

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    blocks={"read_only_allow_delete": False},
    # read_only_allow_delete=False
)

html_strip = analyzer(
    "html_strip",
    tokenizer="lowercase",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"],
)


@INDEX.doc_type
class SectorDocument(Document):
    """Secto Elasticsearch document."""

    id = StringField(
        attr="id",
        analyzer=html_strip,
    )

    __name_fields = {
        "raw": KeywordField(),
        "suggest": fields.CompletionField(),
        "edge_ngram_completion": StringField(analyzer=edge_ngram_completion),
        "mlt": StringField(analyzer="english"),
    }

    name = StringField(analyzer=html_strip, fields=__name_fields)
    # Date created
    created = fields.DateField()

    class Django(object):
        model = Sector  # The model associate with this Document

    class Meta(object):
        parallel_indexing = True
        # queryset_pagination = 50  # This will split the queryset
        #                           # into parts while indexing
