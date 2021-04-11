from rest_framework import serializers
from .. import models
from django.contrib.auth import get_user_model


class OwnProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Employees
        fields = '__all__'
        read_only_fields = ('id', 'school', 'slug', 'created_by', 'user')


class EmployeesSerializer(serializers.ModelSerializer):

    """ Only For Creating New Employees and Listing all of them"""

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
        )
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=99, write_only=True)
    last_name = serializers.CharField(max_length=99, write_only=True)
    middle_name = serializers.CharField(max_length=99, write_only=True)
  

    class Meta:
        model = models.Employees
        fields = '__all__'
        read_only_fields = ('id', 'school', 'slug', 'created_by', 'user')

 
    def create(self, validated_data):
        
        email = validated_data.pop('email')
        f_name = validated_data.pop('first_name')
        l_name = validated_data.pop('last_name')
        m_name = validated_data.pop('middle_name')
        password = validated_data.pop('password')

        user = get_user_model().objects.create_user(
            email = email,
            first_name = f_name,
            last_name = l_name,
            password = password,
            middle_name = m_name
        )

        validated_data['user'] = user   
        instance = super().create(validated_data)

        return instance


class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Courses
        fields = '__all__'
        read_only_fields = ('id',)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Department
        fields = '__all__'
        read_only_fields = ('id', 'school')


class PoliciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Policies
        fields = '__all__'
        read_only_fields = ('id', 'school')


class SchoolSerializer(serializers.ModelSerializer):

    policies = PoliciesSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    courses = CoursesSerializer(many=True, read_only=True)
    employees = EmployeesSerializer(many=True, read_only=True)

    class Meta:
        model = models.School
        fields = (
            'id', 'name', 'vision', 'mission','country',
            'street', 'city', 'zip_code', 'date_funded',
            'policies', 'departments', 'courses' , 'employees',
        )
        read_only_fields = ('id', )
