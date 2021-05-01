from rest_framework import serializers
from .. import models
from django.contrib.auth import get_user_model
from school.models import TeacherSubject


# Serializer for school admin that facilicate students start here

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

class TeacherStudents(serializers.ModelSerializer):

    class Meta:
        model = models.StudentSubject
        fields = '__all__'
        read_only_fields = (
            'id', 'student', 'abs_1', 'abs_2', 'abs_3',
            'period_1', 'period_2', 'period_3', 'avg', 'status'
            )


class TeacherSubjectSerializer(serializers.ModelSerializer):

    """
    Serializer for viewing all of subjects handled by
    logged in teacher/professor
    """
    teacher = serializers.StringRelatedField(read_only=True)
    section = serializers.StringRelatedField(read_only=True)
    schedule = serializers.StringRelatedField(read_only=True)
    # subject = serializers.StringRelatedField(read_only=True)
    student = TeacherStudents(read_only=True, many=True)


    class Meta:
        model = TeacherSubject
        fields = ('id','teacher', 'section', 'schedule', 'subject', 'student')
        read_only_fields = ('id','teacher', 'section', 'schedule', 'subject', )

class StudentSubjectSerializer(serializers.ModelSerializer):

    """
    Serializer for adding new subject on enrolled students
    """

    class Meta:
        model = models.StudentSubject
        fields = '__all__'
        read_only_fields = (
            'id', 'student', 'abs_1', 'abs_2', 'abs_3',
            'period_1', 'period_2', 'period_3', 'avg', 'status'
            )

# Serializer for school admin that facilicate students ends here

# Serializers for student user starts here


class FileAssignmentSerializer(serializers.ModelSerializer):

    """
    Nested serializer for StudentAssignmentSerializer.
    Purpose: Accept file
    """

    class Meta:
        model = models.FileAssignment
        fields = '__all__'
        read_only_fields = ('id', 'assignment', 'student')

    def create(self, validated_data):

        return super().create(validated_data)


class StudentAssignmentSerializer(serializers.ModelSerializer):

    """
    Serializer for students viewing and passing assignments on a
    particular subject
    """

    assignment_files = FileAssignmentSerializer(write_only=True)

    class Meta:
        model = models.Assignment
        fields = (
            'id', 'assignment_files', 'subject', 'title',
            'dead_line', 'description', 'sample', 'assign',
            )
        read_only_fields = (
            'id', 'subject', 'title',
            'dead_line', 'description', 'assign', 'sample'
            )

    def update(self, instance, validated_data):

        user = self.context['request'].user
        subject = instance.subject
        student_sub = models.StudentSubject.objects.get(
            student__user=user,
            subject=subject
            )
        assignment_files = validated_data.pop('assignment_files')
        models.FileAssignment.objects.create(
            **assignment_files,
            assignment=instance,
            student=student_sub
        )

        return super().update(instance, validated_data)


class FileProjectSerializer(serializers.ModelSerializer):

    """
    Nested serializer for StudentProjectSerializer.
    Purpose: Accept file
    """

    class Meta:
        model = models.FileProject
        fields = '__all__'
        read_only_fields = ('id', 'project', 'student')

    def create(self, validated_data):

        return super().create(validated_data)


class StudentProjectSerializer(serializers.ModelSerializer):

    """
    Serializer for students viewing and passing projects on a
    particular subject
    """

    project_file = FileProjectSerializer(write_only=True)

    class Meta:
        model = models.Project
        fields = (
            'id', 'subject', 'title', 'dead_line', 'description',
            'sample', 'assign', 'project_file'
        )
        read_only_fields = (
            'id', 'subject', 'title', 'dead_line', 'description',
            'sample', 'assign',
        )

    def update(self, instance, validated_data):

        user = self.context['request'].user
        subject = instance.subject
        student_sub = models.StudentSubject.objects.get(
            student__user=user,
            subject=subject
            )
        assignment_files = validated_data.pop('project_file')
        models.FileProject.objects.create(
            **assignment_files,
            project=instance,
            student=student_sub
        )

        return super().update(instance, validated_data)


class StudentOwnerSerializer(serializers.ModelSerializer):

    """
    Serializer for viewing the current profile of logged in students.
    """

    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Students
        fields = (
            'id', 'user', 'course', 'pic',
            'school', 'bday', 'country', 'city',
            'zip_code', 'sex', 'civil_status', 'school_yr',
            'sem', 'slug'
            )
        read_only_fields = (
            'id', 'slug', 'sem', 'school_yr',
            'school', 'course', 'user'
            )


class ClassMateSerializer(serializers.ModelSerializer):

    subject = serializers.StringRelatedField(read_only=True)
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.StudentSubject
        fields = ('id', 'subject', 'student')


# Serializers for student user ends here

# Serializers for logged in teacher starts here



class TeacherStudentSerializer(serializers.ModelSerializer):

    """
    Serializer for editing grades and absencees of one student
    """

    student = serializers.StringRelatedField(read_only=True)
    subject = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.StudentSubject
        fields = '__all__'
        read_only_fields = ('id', 'avg')

    def avg(self, *args):

        return float(sum([i for i in args]))/2

    def update(self, instance, validated_data):

        p_1 = int(validated_data.get('period_1'))
        p_2 = int(validated_data.get('period_2'))
        p_3 = int(validated_data.get('period_3'))

        validated_data['avg'] = self.avg(p_1, p_2, p_3)

        status = validated_data.get('status')
        avg = validated_data.get('avg')

        if status == 'INC':
            validated_data['status'] = 'INC'

        elif avg >= 75:
            validated_data['status'] = 'Passed'

        else:
            validated_data['status'] = 'Failed'

        return super().update(instance, validated_data)


class TeacherAssignmentSerializer(serializers.ModelSerializer):

    """
    Serializer for teachers. Adding new assignment on a specific
    subject
    """

    class Meta:
        model = models.Assignment
        fields = (
            'subject', 'title', 'dead_line', 'description', 'assign'
        )
        read_only_fields = ('id', 'subject')


class TeacherProjectSerializer(serializers.ModelSerializer):

    """
    Serializer for teachers. Adding new assignment on a specific
    subject
    """

    class Meta:
        model = models.Project
        fields = (
            'subject', 'title', 'dead_line', 'description', 'assign'
        )
        read_only_fields = ('id', 'subject')

# Serializers for logged in teacher ends here
