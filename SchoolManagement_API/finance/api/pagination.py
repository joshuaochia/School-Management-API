from rest_framework.pagination import PageNumberPagination

class GenericFinancePag(PageNumberPagination):
    page_size = 10