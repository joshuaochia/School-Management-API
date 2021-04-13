from rest_framework import serializers
from .. import models
from django.contrib.auth import get_user_model
from students.models import Subjects, StudentSubject


class OwnProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for editing your own profile as an employee
    """

    class Meta:
        model = models.Employees
        fields = '__all__'
        read_only_fields = ('id', 'school', 'slug', 'created_by', 'user')


class EmployeesSerializer(serializers.ModelSerializer):

    """
    Only For Creating New Employees and Listing all of them
    """

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
            email=email,
            first_name=f_name,
            last_name=l_name,
            password=password,
            middle_name=m_name
        )

        validated_data['user'] = user
        instance = super().create(validated_data)

        return instance


class CoursesSerializer(serializers.ModelSerializer):

    """
    Serializer for Courses model - for editing, adding, and deleting.
    """
    class Meta:
        model = models.Courses
        fields = '__all__'
        read_only_fields = ('id',)


class DepartmentSerializer(serializers.ModelSerializer):

    """
    Serializer for department model - for editing, adding, and deleting.
    """

    class Meta:
        model = models.Department
        fields = '__all__'
        read_only_fields = ('id', 'school')


class PoliciesSerializer(serializers.ModelSerializer):

    """
    Serializer for policies model - for editing, adding, and deleting.
    """

    class Meta:
        model = models.Policies
        fields = '__all__'
        read_only_fields = ('id', 'school')


class SchoolSerializer(serializers.ModelSerializer):

    """
    Serialzier for the school
    """

    policies = PoliciesSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    courses = CoursesSerializer(many=True, read_only=True)
    employees = EmployeesSerializer(many=True, read_only=True)

    class Meta:
        model = models.School
        fields = (
            'id', 'name', 'vision', 'mission', 'country',
            'street', 'city', 'zip_code', 'date_funded',
            'policies', 'departments', 'courses', 'employees',
        )
        read_only_fields = ('id', )


class TeacherSubjectSerializer(serializers.ModelSerializer):

    """
    Serializer for viewing all of subjects handled by
    logged in teacher/professor
    """

    course = serializers.StringRelatedField(read_only=True)
    schedule = serializers.StringRelatedField(read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    section = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subjects
        fields = '__all__'


class TeacherStudentSerializer(serializers.ModelSerializer):

    """
    Serializer for editing grades and absencees of one student
    """

    student = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentSubject
        fields = '__all__'
