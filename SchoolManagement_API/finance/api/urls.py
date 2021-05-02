from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

app_name = 'api_finance'

# Routers for HR's to add payments, OT, or leave.
router = DefaultRouter()
router.register('balance', viewsets.AllStudentBalanceViewSet, basename='balance')
router.register('salary', viewsets.AllEmployeeSalaryViewSet, basename='salary')


urlpatterns = [
    path('', include(router.urls)),

    # Url for viewing user balance if student and salary if employee
    path('my-balance', viewsets.StudentBalanceViewSet.as_view(), name='my-balance'),
    path('my-salary', viewsets.EmployeeSalaryViewSet.as_view(), name='my-salary')
]
