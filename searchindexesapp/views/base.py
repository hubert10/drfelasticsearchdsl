from searchindexesapp.serializers.enterprise import EnterpriseDocumentSimpleSerializer
from searchindexesapp.documents.enterprise import EnterpriseDocument
from elasticsearch_dsl import DateHistogramFacet, RangeFacet
from django_elasticsearch_dsl_drf.viewsets import (
    BaseDocumentViewSet,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)

__all__ = ("BaseEnterpriseDocumentViewSet",)


class BaseEnterpriseDocumentViewSet(BaseDocumentViewSet):
    """Base EnterpriseDocument ViewSet."""

    document = EnterpriseDocument
    serializer_class = EnterpriseDocumentSimpleSerializer
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        FacetedSearchFilterBackend,
        HighlightBackend,
    ]
    # Define search fields
    search_fields = (
        "name",
        "description",
        "summary",
    )
    # Define highlight fields
    highlight_fields = {
        "name": {
            "enabled": True,
            "options": {
                "pre_tags": ["<b>"],
                "post_tags": ["</b>"],
            },
        },
        "summary": {"options": {"fragment_size": 50, "number_of_fragments": 3}},
        "description": {},
    }
    # Define filter fields
    filter_fields = {
        "id": {
            "field": "id",
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
                LOOKUP_FILTER_TERMS,
            ],
        },
        "name": "name.raw",
        "summary": "summary",
        "created": "created",
        "skills": {
            "field": "skills",
            "lookups": [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
        "skills.raw": {
            "field": "skills.raw",
            "lookups": [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }
    # Post filter fields, copy filters as they are valid
    post_filter_fields = {
        "skills_pf": {
            "field": "skills",
            "lookups": [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
        "skills_raw_pf": {
            "field": "skills.raw",
            "lookups": [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        "id": "id",
        "name": "name.raw",
        "created": "created",
    }
    # Specify default ordering
    ordering = (
        "id",
        "title",
        "price",
    )
    faceted_search_fields = {
        "created": {
            "field": "created",
            "facet": DateHistogramFacet,
            "options": {
                "interval": "year",
            },
        },
    }
