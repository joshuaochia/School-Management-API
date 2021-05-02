from django.http import HttpResponse
from rest_framework import (
    viewsets, status, permissions, authentication, generics, filters
    )
from .. import models
from students.models import Students
from . import serializers, permissions as perm
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import pagination as pag
from school.models import Employees
from school.api.serializers import EmployeesSerializer
from django.core.exceptions import *


class AllStudentBalanceViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.StudentBalanceSerializer
    permission_classes = (perm.IsHROnly, )
    serializer_class_by_action = {
        'payment': serializers.StudentPaymentsSerializer
    }
    permission_classes_by_action = {
        'payment': [perm.IsHROnly()],
    }
    
    def get_queryset(self):

        return models.StudentBalance.objects.all()

 
    def get_serializer_class(self):

        try:
            return self.serializer_class_by_action[self.action]
        except KeyError:
            return super().get_serializer_class()
    
    def get_permissions(self):

        try:
            return self.permission_classes_by_action[self.action]
        except KeyError:
            return super().get_permissions()


    @action(detail=True, methods=['GET', 'POST'], url_path='payment')
    def payment(self, request, pk=None):

        student_bal = self.get_object()
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save(balance=student_bal)
                return Response(serializer.data)
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentBalanceViewSet(generics.RetrieveAPIView):

    serializer_class = serializers.StudentBalanceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        
        student = get_object_or_404(Students, user=self.request.user)
        return get_object_or_404(models.StudentBalance, student=student)


class AllEmployeeSalaryViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.EmployeeSalarySerializer
    permission_classes = (perm.IsHROnly,)

    permission_classes_by_action = {
        'payment': [perm.IsHROnly()],
    }

    serializer_class_by_action = {
        'overtime': serializers.EmployeeOTSerializer,
        'leave': serializers.EmployeeLeaveSerializer
    }

    def get_queryset(self):

        return Employees.objects.all()

    def get_serializer_class(self):

        try:
            return self.serializer_class_by_action[self.action]
        except KeyError:
            return super().get_serializer_class()

    def get_permissions(self):

        try:
            return self.permission_classes_by_action[self.action]
        except KeyError:
            return super().get_permissions()


    @action(detail=True, methods=['GET', 'POST'], url_path='overtime')
    def overtime(self, request, pk=None):

        employee = self.get_object()
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save(salary=employee)
                return Response(serializer.data)
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'POST'], url_path='leave')
    def leave(self, request, pk=None):

        employee = self.get_object()
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save(salary=employee)
                return Response(serializer.data)
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeSalaryViewSet(generics.RetrieveAPIView):

    serializer_class = serializers.EmployeeSalarySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Employees, user=user)
