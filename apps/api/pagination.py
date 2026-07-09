"""
API Pagination classes for ZimTechHub.
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination with configurable page size.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Large result set pagination for data-heavy endpoints.
    """
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class SmallResultsSetPagination(PageNumberPagination):
    """
    Small result set pagination for lightweight endpoints.
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
