from rest_framework.pagination import PageNumberPagination


class EmployeesPageLimit(PageNumberPagination):
    page_size = 20
