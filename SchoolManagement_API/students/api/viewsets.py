from rest_framework import (
    viewsets, status, pagination, generics
    )
from .. import models
from . import serializers, permissions as perm
from .pagination import PageLimit
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


class TeacherViewSets(viewsets.ModelViewSet):

    """
    Add a student grade and edit
    """


class SubjectViewSet(viewsets.ModelViewSet):

    """
    Add, edit, delete, etc.. a new subject for students to populate

    Permission: Only admin can add users
    """

    queryset = models.Subjects.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly,)

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

    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = PageLimit
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['day', ]


class SectionViewSet(viewsets.ModelViewSet):

    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = pagination.LimitOffsetPagination


class GradesViewSet(viewsets.ViewSet):

    """
    Viewset only for students to view thei  r grades and schedule
    """

    def list(self, request):
        user = self.request.user
        query = models.StudentSubject.objects.filter(student__user=user)
        serializer = serializers.StudentSubjectSerializer(query, many=True)

        return Response(serializer.data)


class StudentProfile(generics.RetrieveUpdateDestroyAPIView):

    """
    Viewsset for viewing or updating the curret logged in student profile
    """

    serializer_class = serializers.StudentOwnerSerializer

    def get_object(self):
        return get_object_or_404(models.Students, user=self.request.user)
