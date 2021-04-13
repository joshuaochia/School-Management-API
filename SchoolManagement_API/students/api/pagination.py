from rest_framework.pagination import (
    PageNumberPagination,
    )


class PageLimit(PageNumberPagination):
    page_size = 10


class StudentLimit(PageNumberPagination):
    page_size = 20
    page_query_param = 'students'
