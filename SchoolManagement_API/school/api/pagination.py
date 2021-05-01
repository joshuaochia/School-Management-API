from rest_framework.pagination import PageNumberPagination


class EmployeesPageLimit(PageNumberPagination):
    page_size = 20


class PageLimit(PageNumberPagination):
    page_size = 10


class StudentLimit(PageNumberPagination):
    page_size = 20
    page_query_param = 'students'
