"""
This file provides an Pagination classes that are the used for all list views for determine the structure of the output that should
be used for paginated responses.
"""

from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.pagination import (
    PageNumberPagination,
    CursorPagination,
    LimitOffsetPagination,
    _get_displayed_page_numbers,
    _get_page_links,
)
from collections import OrderedDict, namedtuple
from rest_framework.response import Response


class SearchResultsPagination(PageNumberPagination):
    """
    Returns the paginated search results with Elasticsearch
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )

    def get_next_link(self):
        """
        Given a list of page numbers and `None` page breaks,
        return a list of `PageLink` objects with the next page.
        """
        if not self.page.has_next():
            return None
        url_http = self.request.build_absolute_uri()

        # The basic class supports 'http' so we can make some modification for supporting 'https'
        url = url_http
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        """
        Given a list of page numbers and `None` page breaks,
        return a list of `PageLink` objects with the previous page.
        """
        if not self.page.has_previous():
            return None
        url_http = self.request.build_absolute_uri()

        # The basic class supports 'http' so we can make some modification for supporting 'https'
        url = url_http
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
