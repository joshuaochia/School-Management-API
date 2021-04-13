from students.models import Subjects, StudentSubject
from rest_framework import (
    viewsets, status, permissions, authentication, generics, filters
    )
from .. import models
from . import serializers, permissions as perm
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class SchoolViewSet(viewsets.ModelViewSet):

    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, )
    action_method = ['POST', 'GET', 'PATCH', 'DELETE']

    def get_serializer_class(self):

        if self.action == 'policies':
            return serializers.PoliciesSerializer
        if self.action == 'departments':
            return serializers.DepartmentSerializer
        if self.action == 'courses':
            return serializers.CoursesSerializer

        return self.serializer_class

    def filtering(self, request, querys):
        """
        Function for filtering using ?id={pk} (Feature: Update or Delete)
        The filtered model.
        """
        serializer = self.get_serializer(querys)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                querys,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if request.method == 'DELETE':
            querys.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data)

    def actionhelper(self, request, query, obj):
        """
        Helper for @action decoration POST or Delete Method
        """

        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save(school=obj)
            return Response(serializer.data)

        if request.method == 'DELETE':
            query.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=action_method, url_path='policies')
    def policies(self, request, pk=None):

        obj = self.get_object()
        query = models.Policies.objects.filter(school=obj)
        serializer = self.get_serializer(query, many=True)

        # Filter a Policy object (Feature: Delete, Update)
        id = self.request.query_params.get('id')

        if id:
            filter_object = get_object_or_404(models.Policies, id=id)
            return self.filtering(request, filter_object)

        # Post and Delete Method
        self.actionhelper(request, query, obj)

        return Response(serializer.data)

    @action(detail=True, methods=action_method, url_path='departments')
    def departments(self, request, pk=None):

        obj = self.get_object()
        query = models.Department.objects.filter(school=obj)
        serializer = self.get_serializer(query, many=True)

        # Filter a Department object (Feature: Delete, Update)
        id = self.request.query_params.get('id')

        if id:
            filter_object = get_object_or_404(models.Department, id=id)
            return self.filtering(request, filter_object)

        # Post and Delete Method
        self.actionhelper(request, query, obj)

        return Response(serializer.data)

    @action(detail=True, methods=action_method, url_path='courses')
    def courses(self, request, pk=None):

        obj = self.get_object()
        query = models.Courses.objects.filter(school=obj)
        serializer = self.get_serializer(query, many=True)

        # Filtering base on ID
        id = self.request.query_params.get('id')

        if id:
            filter_object = get_object_or_404(models.Courses, id=id)
            return self.filtering(request, filter_object)

        # Post and Delete Method
        self.actionhelper(request, query, obj)

        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = models.Employees.objects.all()
    serializer_class = serializers.EmployeesSerializer
    permission_classes = (perm.EmployeeOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['=position', ]

    def perform_create(self, serializer):

        user = self.request.user
        school = get_object_or_404(models.School, pk=1)
        return serializer.save(created_by=user, school=school)


class OwnProfileViewSet(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.OwnProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(models.Employees, user=self.request.user)


class TeacherSubjectViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.TeacherSubjectSerializer

    def get_queryset(self):

        user = self.request.user
        return Subjects.objects.filter(teacher__user=user)

    def get_serializer_class(self):

        if self.action == 'students':
            return serializers.TeacherStudentSerializer

        return self.serializer_class

    @action(detail=True, methods=['GET', 'PUT'], url_path='students')
    def students(self, request, pk=None):

        instance = self.get_object()
        user = self.request.user
        query = StudentSubject.objects.filter(
            subject__teacher__user=user,
            subject=instance
            )

        id = self.request.query_params.get('id')

        if id:
            q = get_object_or_404(StudentSubject, pk=id, subject=instance)
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
