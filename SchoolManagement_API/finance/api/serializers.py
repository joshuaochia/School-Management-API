from django.shortcuts import get_object_or_404
from .. import models
from rest_framework import serializers


class StudentBalanceSerializer(serializers.ModelSerializer):

    """
    Serialzier for students balances
    """
    class Meta:
        model = models.StudentBalance
        fields = ('__all__')


class StudentPaymentsSerializer(serializers.ModelSerializer):

    """
    Serializer for students each payments
    """

    class Meta:
        model = models.StudentPayment
        fields = ('__all__')
        read_only_fields = ('id', 'balance')


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


