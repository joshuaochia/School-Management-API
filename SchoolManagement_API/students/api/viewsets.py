from rest_framework import (
    viewsets, status, generics,
    permissions
    )
from .. import models
from . import serializers, permissions as perm
from .pagination import PageLimit, StudentLimit
from rest_framework.decorators import action
from rest_framework.response import Response
from school.models import School
from rest_framework import filters
from django.shortcuts import get_object_or_404


class StudentsViewSets(viewsets.ModelViewSet):

    """ Viewset for creating new students with action of adding, deleting, and
        editing (Subject, section, and schedule).

        Permission: Only Admin can do this
    """

    queryset = models.Students.objects.all()
    serializer_class = serializers.StudentsSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = StudentLimit

    def get_serializer_class(self):

        if self.action == 'subject':
            return serializers.StudentSubjectSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        obj = get_object_or_404(School, pk=1)
        return serializer.save(school=obj)

    def actionhelper(self, request, query, obj):

        """
        Helper for @action decoration POST or Delete Method
        """

        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(student=obj)
            return Response(serializer.data)

        if request.method == 'DELETE':
            query.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'GET'], detail=True, url_path='add-subject')
    def subject(self, request, pk=None):

        obj = self.get_object()
        query = models.StudentSubject.objects.filter(student=obj)
        serializer = self.get_serializer(query, many=True)

        self.actionhelper(request, query, obj)

        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):

    """
    Add, edit, delete, etc.. a new subject for students to populate
    Permission: Only admin can add new subjects
    """

    queryset = models.Subjects.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly,)
    pagination_class = PageLimit

    def get_serializer_class(self):

        if self.action == 'schedule':
            return serializers.ScheduleSerializer

        return self.serializer_class

    def actionhelper(self, request, query, obj):
        """
        Helper for @action decoration POST or Delete Method
        """
        if request.method == 'DELETE':
            query.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                query,
                data=request.data,
                partial=True,
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(methods=['GET', 'PATCH', ], detail=True, url_path='schedule')
    def schedule(self, request, pk=None):

        obj = self.get_object()
        query = models.Schedule.objects.get(subject=obj)
        serializer = self.get_serializer(query)

        self.actionhelper(request, query, obj)

        return Response(serializer.data)


class ScheduleViewSet(viewsets.ModelViewSet):

    """
    Creating, editing, deleting new schedule for students
    Permission: Only admin can add new subjects
    """

    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = PageLimit
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['day', ]


class SectionViewSet(viewsets.ModelViewSet):

    """
    Viewset for adding, deleting, and editing new section for the students
    Permission: Only admin can add new subjects
    """

    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = PageLimit


class GradesViewSet(viewsets.ViewSet):

    """
    Viewset only for students to view their grades and schedule
    """
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageLimit

    def list(self, request):
        user = self.request.user
        query = models.StudentSubject.objects.filter(student__user=user)
        serializer = serializers.StudentSubjectSerializer(query, many=True)

        return Response(serializer.data)


class TeacherSubjectViewSet(viewsets.ModelViewSet):

    """
    Viewset for viewing all the subjects handled by a teacher and there's
    a feature of adding grades and absencees for each students
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.TeacherSubjectSerializer

    def get_queryset(self):

        user = self.request.user
        return models.Subjects.objects.filter(teacher__user=user)

    def get_serializer_class(self):

        if self.action == 'students':
            return serializers.TeacherStudentSerializer

        return self.serializer_class

    @action(detail=True, methods=['GET', 'PUT'], url_path='students')
    def students(self, request, pk=None):

        instance = self.get_object()
        user = self.request.user
        query = models.StudentSubject.objects.filter(
            subject__teacher__user=user,
            subject=instance
            )

        id = self.request.query_params.get('id')

        if id:
            q = get_object_or_404(
                models.StudentSubject,
                pk=id,
                subject=instance
                )
            serializer = self.get_serializer(q)
            if request.method == 'PUT':
                serializer = self.get_serializer(
                    q,
                    data=request.data,
                    partial=True,
                    )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(query, many=True)

        return Response(serializer.data)


class StudentProfile(generics.RetrieveUpdateDestroyAPIView):

    """
    Viewsset for viewing or updating the curret logged in student profile
    """

    serializer_class = serializers.StudentOwnerSerializer

    def get_object(self):
        return get_object_or_404(models.Students, user=self.request.user)


class ClassMateViewSet(viewsets.ModelViewSet):

    """
    Viewset for viewing all the classmate on specific subject
    """

    serializer_class = serializers.ClassMateSerializer

    def get_queryset(self):

        user = self.request.user
        query = models.StudentSubject.objects.filter(student__user=user)
        return query

    def get_serializer_class(self):

        if self.action == 'classmates':
            return serializers.StudentOwnerSerializer

        return self.serializer_class

    @action(methods=['GET', ], detail=True, url_path='classmates')
    def classmates(self, request, pk=None):

        obj = self.get_object()
        query = models.Students.objects.filter(student_sub=obj)
        serializer = self.get_serializer(query, many=True)

        return Response(serializer.data)
