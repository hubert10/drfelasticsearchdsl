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
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from searchindexesapp.documents.enterprise import EnterpriseDocument
from searchindexesapp.serializers.enterprise import EnterpriseDocumentSerializer
from drfelasticsearchdsl.core.customer_pagination import SearchResultsPagination
from drfelasticsearchdsl.core.search_querysets import QuerySetChain
from enterprisesapp.models.enterprise_saved_search import EnterpriseSavedSearch
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl.query import MultiMatch, Match
from elasticsearch_dsl import Q
from drfelasticsearchdsl.tasks import (
    task_create_enterprise_saved_searches_in_background,
)


class EnterpriseDocumentViewSet(DocumentViewSet):
    """The Enterprise Document view."""

    document = EnterpriseDocument
    serializer_class = EnterpriseDocumentSerializer
    lookup_field = "id"
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # Define search fields
    search_fields = (
        "name",
        "description",
        "summary",
    )
    # Define filter fields
    filter_fields = {
        "skills": {
            "field": "skills",
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
        "skills.raw": {
            "field": "skills.raw",
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
        "sectors": {
            "field": "sectors",
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
        "sectors.raw": {
            "field": "sectors.raw",
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

    def list(self, request, *args, **kwargs):
        """
        Returns the filters results data for every request
        """
        enterprises = []
        # We get the application client id
        import django

        lan = django.utils.translation.get_language()

        if (
            (request.GET.get("q") is None)
            and (request.GET.get("FacetSkill") is None)
            and (request.GET.get("FacetSector") is None)
        ):

            queryset = super(EnterpriseDocumentViewSet, self).get_queryset().filter()
            paginator = SearchResultsPagination()
            # queryset1 = queryset.filter(Q("match_phrase", name='test99999'))
            # queryset2 = queryset.exclude(Q("match_phrase", name='test99999'))
            # from queryset_sequence import QuerySetSequence
            # queryset = QuerySetSequence(queryset1, queryset2)

            # order = 0
            # for enterprise in queryset[:10000]:
            #     task_create_enterprise_saved_searches_in_background.delay(enterprise["name"], order)
            #     order += 1

            # from itertools import chain
            # queryset = list(chain(queryset1, queryset2))
            # queryset = QuerySetChain(queryset1, queryset2)
            # print(type(queryset2))

            # print(queryset1.count())
            # print(queryset2.count())
            # print(len(queryset))
            # queryset = queryset1 + queryset2

            queryset = paginator.paginate_queryset(queryset, request)
            enterprises = []

            for entreprise in queryset:
                enterprises.append(
                    {
                        "name": entreprise["name"],
                        "summary": entreprise["summary"],
                        "description": entreprise["description"],
                        "skills": [
                            skill for skill in entreprise["skills" + "_" + str(lan)]
                        ],
                        "sectors": [
                            sector for sector in entreprise["sectors" + "_" + str(lan)]
                        ],
                    }
                )

            results = {
                "enterprises": enterprises,
            }
            # results = list()
            self._paginator = paginator
            return paginator.get_paginated_response(results)
            # return Response(results)
        else:
            query = self.request.GET.get("q", "")
            query_sector = self.request.GET.get("FacetSector", "")
            query_skill = self.request.GET.get("FacetSkill", "")

            queryset = super(EnterpriseDocumentViewSet, self).get_queryset()

            if query:
                from searchindexesapp.analyzers import html_strip, custom_analyzer

                # No need to lowercasing received query string, check on your mappings

                # Search
                or_lookup = Q("match_phrase", name=query) | Q(
                    "match_phrase", description=query
                )
                queryset = queryset.query(or_lookup)

            if query_skill and queryset:
                queryset = queryset.filter(
                    Q("match_phrase", skills_en=query_skill.lower())
                    | Q("match_phrase", skills_fr=query_skill.lower())
                    | Q("match_phrase", skills=query_skill)
                )

            if query_sector and queryset:
                queryset = queryset.filter(
                    Q("match_phrase", sectors_en=query_sector.lower())
                    | Q("match_phrase", sectors_fr=query_sector.lower())
                )

            # queryset = queryset.order_by('company_score')

            paginator = SearchResultsPagination()
            queryset = paginator.paginate_queryset(queryset, request)

            enterprises = []

            for entreprise in queryset:
                enterprises.append(
                    {
                        "name": entreprise["name"],
                        "summary": entreprise["summary"],
                        "description": entreprise["description"],
                        "skills": [
                            skill for skill in entreprise["skills" + "_" + str(lan)]
                        ],
                        "sectors": [
                            sector for sector in entreprise["sectors" + "_" + str(lan)]
                        ],
                    }
                )
            results = {
                "enterprises": enterprises,
            }
            self._paginator = paginator
            return paginator.get_paginated_response(results)
