from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_EXISTS,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_FILTER_REGEXP,
    LOOKUP_QUERY_CONTAINS,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_STARTSWITH,
    LOOKUP_QUERY_ENDSWITH,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from searchindexesapp.documents.skill import SkillDocument
from searchindexesapp.serializers.skill import SkillDocumentSerializer
from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
)


class SkillDocumentView(DocumentViewSet):
    """The Skill Document view."""

    document = SkillDocument
    serializer_class = SkillDocumentSerializer
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]
    # # Define search fields
    # search_fields = {
    #     "name": {
    #         "field": "name",
    #         # Note, that we limit the lookups of `name` field in this
    #         # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
    #         "lookups": [
    #             LOOKUP_QUERY_CONTAINS,
    #         ],
    #     },
    # }
    # Define filter fields
    filter_fields = {
        "name": {
            "field": "name",
            # Note, that we limit the lookups of `name` field in this
            # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
            "lookups": [
                LOOKUP_QUERY_ENDSWITH,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        "name.raw": {
            "field": "name.raw",
            # Note, that we limit the lookups of `name` field in this
            # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
            "lookups": [
                LOOKUP_QUERY_CONTAINS,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
        "created": "created",
    }
    # Define ordering fields
    ordering_fields = {
        "name": "name.raw",
        "created": "created",
    }
    # Specify default ordering
    ordering = ("created",)

    suggester_fields = {
        "name_suggest": {
            "field": "name.suggest",
            "suggesters": [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
            "default_suggester": SUGGESTER_COMPLETION,
        },
    }
