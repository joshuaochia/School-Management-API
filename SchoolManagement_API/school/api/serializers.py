from rest_framework import serializers
from .. import models
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin



class OwnProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for editing your own profile as an employee
    """
    school = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Employees
        fields = (
            'id', 'bday', 'city', 'zip_code',
            'sex', 'civil_status', 'department',
            'school',  'user', 'slug'
            )
        read_only_fields = ('id', 'school', 'user', 'department')


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
        read_only_fields = (
            'id','school', 'slug', 'created_by',
            'user', 'is_hr', 'is_employee', 'is_teacher'
            )

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

        position = validated_data.get('position')
        if position == 'Teacher':
            validated_data['is_teacher'] = True
        if position == 'HR':
            validated_data['is_hr'] = True

        return super().create(validated_data)


class CoursesSerializer(serializers.ModelSerializer):

    """
    Serializer for Courses model - for editing, adding, and deleting.
    """
    class Meta:
        model = models.Courses
        fields = '__all__'
        read_only_fields = ('id', 'school')


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


class SchoolSerializer(CountryFieldMixin, serializers.ModelSerializer):

    """
    Serialzier for the school
    """

    policies = PoliciesSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    courses = CoursesSerializer(many=True, read_only=True)

    class Meta:
        model = models.School
        fields = (
            'id', 'name', 'vision', 'mission', 'country',
            'street', 'city', 'zip_code', 'date_funded',
            'policies', 'departments', 'courses', 'employees',
        )
        read_only_fields = ('id', )




class SectionSerializer(serializers.ModelSerializer):

    """
    Save new student.models.section or edit existing one
    """

    class Meta:
        model = models.Section
        fields = '__all__'
        read_only_fields = ('id',)


class ScheduleSerializer(serializers.ModelSerializer):

    """
    Save new student.models.Schedule or edit existing one
    """

    class Meta:
        model = models.Schedule
        fields = '__all__'
        read_only_fields = ('id',)

class SubjectSerializer(serializers.ModelSerializer):

    """
    Create new subject for the school.
    Also: Nested serializer for StudentSubjectSerializer for reading
    """

    schedule = serializers.StringRelatedField(read_only=True)
    section = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Subjects
        fields = '__all__'
        read_only_fields = ('id',)

class TeacherAddSubject(serializers.ModelSerializer):

    section = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)
    schedule = serializers.StringRelatedField(read_only=True)
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Section.objects.all(),
        write_only=True
        )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Subjects.objects.all(),
        write_only=True
        )
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Schedule.objects.all(),
        write_only=True 
        )

    class Meta:
        model = models.TeacherSubject
        fields = '__all__'
        read_only_fields = ('id', 'teacher')

    def create(self, validated_data):

        
        section_id = validated_data.pop('section_id')
        schedule_id = validated_data.pop('schedule_id')
        subject_id = validated_data.pop('subject_id')

        validated_data['subject'] = subject_id
        validated_data['section'] = section_id
        validated_data['schedule'] = schedule_id

        q = models.TeacherSubject.objects.create(**validated_data)

        return q