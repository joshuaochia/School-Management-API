from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

app_name = 'api_finance'

# Routers for admins to edit certain things for students
router = DefaultRouter()
router.register('balance', viewsets.StudentBalanceViewSet, basename='balance')
router.register('salary', viewsets.EmployeeSalaryViewSet, basename='salary')

urlpatterns = [
    path('', include(router.urls))
]
