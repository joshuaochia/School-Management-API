from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

router = DefaultRouter()
router.register('detail', viewsets.SchoolViewSet, basename='school')
router.register('employees', viewsets.EmployeeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'employee/me/',
        viewsets.OwnProfileViewSet.as_view(),
        name='employee_me'
        )
]
