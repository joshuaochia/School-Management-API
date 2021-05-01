from rest_framework import (
    viewsets, status, permissions, authentication, generics, filters
    )
from .. import models
from . import serializers, permissions as perm
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import pagination as pag
from django.core.exceptions import ObjectDoesNotExist
from school.models import Employees
from school.api.serializers import EmployeesSerializer


class StudentBalanceViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.StudentBalanceSerializer
    permission_classes = (perm.IsHROnly, )
    serializer_class_by_action = {
        'payment': serializers.StudentPaymentsSerializer
    }
    permission_classes_by_action = {
        'payment': [perm.IsHROnly()],
    }
    
    def get_queryset(self):

        user = self.request.user
        hr = get_object_or_404(Employees, user=user)
        if user.is_superuser:
                return models.StudentBalance.objects.all()
        if hr.is_hr:
                return models.StudentBalance.objects.all()

        return models.StudentBalance.objects.filter(student__user=user)


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
        query = models.StudentPayment(balance=student_bal)
        serializers = self.get_serializer(query, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(balance=student_bal)

        return Response(serializers.data)


class EmployeeSalaryViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeesSerializer
    permission_classes = (perm.IsSuperUserOrReadOnly,)

    permission_classes_by_action = {
        'overtime': [perm.IsSuperUser()],
        'leave': [perm.IsSuperUser()],
    }

    serializer_class_by_action = {
        'overtime': serializers.EmployeeOTSerializer,
        'leave': serializers.EmployeeLeaveSerializer
    }

    def get_queryset(self):

        user = self.request.user
        queryset = Employees.objects.filter(user=user)
        if user.is_superuser:
            return Employees.objects.all()

        return queryset

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
        query = models.EmployeeOT(salary=employee)
        serializers = self.get_serializer(query, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(salary=employee)

        return Response(serializers.data)

    @action(detail=True, methods=['GET', 'POST'], url_path='leave')
    def leave(self, request, pk=None):

        employee = self.get_object()
        query = models.EmployeeLeave(salary=employee)
        serializers = self.get_serializer(query, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(salary=employee)

        return Response(serializers.data)