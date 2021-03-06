from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets


app_name = 'api_school'

router = DefaultRouter()
router.register('institution', viewsets.SchoolViewSet, basename='institution')
router.register(
    'all-employees',
    viewsets.EmployeeViewSet,
    basename='employees'
    )
router.register(
    'subject',
    viewsets.SubjectViewSet,
    basename='admin_subject'
    )
router.register(
    'schedule',
    viewsets.ScheduleViewSet,
    basename='admin_sched'
    )
router.register(
    'section',
    viewsets.SectionViewSet
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'employee/me/',
        viewsets.OwnProfileViewSet.as_view(),
        name='employee_me'
        )
]
