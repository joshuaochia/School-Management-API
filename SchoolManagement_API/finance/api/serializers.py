from django.shortcuts import get_object_or_404
from .. import models
from rest_framework import serializers
from school.models import Employees

class StudentPaymentsSerializer(serializers.ModelSerializer):

    """
    Serializer for students each payments
    """

    class Meta:
        model = models.StudentPayment
        fields = ('__all__')
        read_only_fields = ('id', 'balance', 'created')

class StudentBalanceSerializer(serializers.ModelSerializer):

    """
    Serialzier for students balances
    """
    payment = StudentPaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = models.StudentBalance
        fields = ('__all__')


class EmployeeOTSerializer(serializers.ModelSerializer):

    """

    """

    class Meta:
        model = models.EmployeeOT
        fields = ('__all__')
        read_only_fields = ('id', 'salary')
    


class EmployeeLeaveSerializer(serializers.ModelSerializer):

    """

    """

    class Meta:
        model = models.EmployeeLeave
        fields = ('__all__')
        read_only_fields = ('id', 'salary')


class EmployeeSalarySerializer(serializers.ModelSerializer):

    overtime = EmployeeOTSerializer(many=True, read_only=True)
    leave = EmployeeLeaveSerializer(many=True, read_only=True)

    class Meta:
        model = Employees
        fields = ('id', 'salary', 'days_week', 'rate', 'overtime', 'leave')
        read_only_fields = ('id',   'overtime', 'leave')