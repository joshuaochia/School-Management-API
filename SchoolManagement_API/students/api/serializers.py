from rest_framework import serializers
from .. import models
from django.contrib.auth import get_user_model


class StudentsSerializer(serializers.ModelSerializer):

    """
    Creating new students with specific course and School - It also take few
    personal data such as birth day, country, sex, etc... After the student
    model is created a AUTH_USER_MODEL designated for the specific student
    will automatically created using the data coming from this serializer.
    Go to students.models.Students for the hardcode
    """

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
        )
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=99, write_only=True)
    last_name = serializers.CharField(max_length=99, write_only=True)
    middle_name = serializers.CharField(max_length=99, write_only=True)
    course = serializers.StringRelatedField(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Courses.objects.all(),
        write_only=True
    )

    class Meta:
        model = models.Students
        fields = (
            'id', 'user', 'school', 'pic',
            'course', 'bday', 'country',
            'city', 'zip_code', 'sex', 'civil_status', 'slug',
            'password', 'email', 'first_name', 'last_name', 'middle_name',
            'course_id'

            )
        read_only_fields = ('id', 'user', 'school', 'slug')

    def create(self, validated_data):

        email = validated_data.pop('email')
        f_name = validated_data.pop('first_name')
        l_name = validated_data.pop('last_name')
        m_name = validated_data.pop('middle_name')
        password = validated_data.pop('password')
        course_id = validated_data.pop('course_id')
        # course = validated_data.pop('course')

        user = get_user_model().objects.create_user(
            email=email,
            first_name=f_name,
            last_name=l_name,
            password=password,
            middle_name=m_name,
        )

        validated_data['user'] = user
        validated_data['course'] = course_id

        return models.Students.objects.create(**validated_data)


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
    Create new subject for a specific user
    """

    schedule = serializers.StringRelatedField(read_only=True)
    section = serializers.StringRelatedField(read_only=True)
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Schedule.objects.all(),
        write_only=True
        )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Section.objects.all(),
        write_only=True
        )

    class Meta:
        model = models.Subjects
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):

        schedule_id = validated_data.pop('schedule_id')
        section_id = validated_data.pop('section_id')

        validated_data['schedule'] = schedule_id
        validated_data['section'] = section_id

        return models.Subjects.objects.create(**validated_data)


class StudentSubjectSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Subjects.objects.all(),
        write_only=True
        )

    class Meta:
        model = models.StudentSubject
        fields = '__all__'
        read_only_fields = ('id', 'student', 'abs', 'grade')

    def create(self, validated_data):

        subject_id = validated_data.pop('subject_id')
        validated_data['subject'] = subject_id

        return models.StudentSubject.objects.create(**validated_data)


class GradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSubject
        fields = '__all__'


class StudentOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Students
        fields = (
            'id', 'user', 'pic', 'course',
            'school', 'bday', 'country', 'city',
            'zip_code', 'sex', 'civil_status', 'school_yr',
            'sem', 'slug'
            )
        read_only_fields = (
            'id', 'slug', 'sem', 'school_yr',
            'school', 'course', 'user'
            )
