from rest_framework.pagination import (
    PageNumberPagination,
    )


class PageLimit(PageNumberPagination):
    page_size = 5
    page_query_param = 'section'
