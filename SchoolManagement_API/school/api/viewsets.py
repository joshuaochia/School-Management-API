from msilib.schema import Error
from rest_framework import (
    viewsets, status, permissions, authentication, generics, filters
    )
from .. import models
from . import serializers, permissions as perm
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import pagination as pag


class BaseAttrViewSet(viewsets.ModelViewSet):

    authentication_classes = (authentication.TokenAuthentication, )

    def get_serializer_class(self):

        try:
            return self.serializer_class_by_action[self.action]
        except:
            return super().get_serializer_class()

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

    def actionhelper(self, request, query, obj_map):
        """
        Helper for @action decoration POST or Delete Method
        """

        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save(**obj_map)
            return Response(serializer.data)

        if request.method == 'DELETE':
            query.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class SchoolViewSet(BaseAttrViewSet):

    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    authentication_classes = (authentication.TokenAuthentication, )
    action_method = ['POST', 'GET', 'PATCH', 'DELETE']

    serializer_class_by_action = {
        'policies': serializers.PoliciesSerializer,
        'departments': serializers.DepartmentSerializer,
        'courses': serializers.CoursesSerializer
    }


    @action(detail=True, methods=action_method, url_path='policies')
    def policies(self, request, pk=None):

        obj = self.get_object()
        obj_map = {
            'school': obj
        }

        try:
            query = models.Policies.objects.filter(school=obj)
            serializer = self.get_serializer(query, many=True)

        # Filter a Policy object (Feature: Delete, Update)
            id = self.request.query_params.get('id')

            if id:
                filter_object = get_object_or_404(models.Policies, id=id)
                return self.filtering(request, filter_object)

        # Post and Delete Method
            self.actionhelper(request, query, obj_map)

            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=action_method, url_path='departments')
    def departments(self, request, pk=None):

        obj = self.get_object()
        obj_map = {
            'school': obj
        }
        try:
            query = models.Department.objects.filter(school=obj)
            serializer = self.get_serializer(query, many=True)

        # Filter a Department object (Feature: Delete, Update)
            id = self.request.query_params.get('id')

            if id:
                filter_object = get_object_or_404(models.Department, id=id)
                return self.filtering(request, filter_object)
        # Post and Delete Method

            self.actionhelper(request, query, obj_map)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=action_method, url_path='courses')
    def courses(self, request, pk=None):

        obj = self.get_object()
        obj_map = {
            'school': obj
        }

        try:
            query = models.Courses.objects.filter(school=obj)
            serializer = self.get_serializer(query, many=True)

        # Filtering base on ID
            id = self.request.query_params.get('id')

            if id:
                filter_object = get_object_or_404(models.Courses, id=id)
                return self.filtering(request, filter_object)

        # Post and Delete Method
            self.actionhelper(request, query, obj_map)

            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(BaseAttrViewSet):

    queryset = models.Employees.objects.all().order_by('-id')
    serializer_class = serializers.EmployeesSerializer
    permission_classes = (perm.EmployeeOrReadOnly, )
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['=position', ]
    pagination_class = (pag.EmployeesPageLimit)

    serializer_class_by_action = {
        'add_subject': serializers.TeacherAddSubject,
    }

    def perform_create(self, serializer):

        user = self.request.user
        school = get_object_or_404(models.School, pk=1)
        return serializer.save(created_by=user, school=school)

    @action(detail=True, methods=['GET', 'POST'], url_path='add-subject')
    def add_subject(self, request, pk=None):
        
        teacher = self.get_object()
        obj_map = {
            'teacher': teacher
        }

        try:
            query = models.TeacherSubject.objects.filter(teacher=teacher)
            serializer = self.get_serializer(query, many=True)
            self.actionhelper(request, query, obj_map)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OwnProfileViewSet(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = serializers.OwnProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(models.Employees, user=self.request.user)


class SubjectViewSet(viewsets.ModelViewSet):

    """
    Add, edit, delete, etc.. a new subject.
    Permission: Only admin can add new subjects
    """

    queryset = models.Subjects.objects.all().order_by('-id')
    serializer_class = serializers.SubjectSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly,)
    pagination_class = pag.PageLimit

class ScheduleViewSet(viewsets.ModelViewSet):

    """
    Creating, editing, deleting new schedule for students
    Permission: Only admin can add new subjects
    """

    queryset = models.Schedule.objects.all().order_by('-id')
    serializer_class = serializers.ScheduleSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = pag.PageLimit
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['day', ]


class SectionViewSet(viewsets.ModelViewSet):

    """
    Viewset for adding, deleting, and editing new section for the students
    Permission: Only admin can add new subjects
    """

    queryset = models.Section.objects.all().order_by('-id')
    authentication_classes = (authentication.TokenAuthentication, )
    serializer_class = serializers.SectionSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = pag.PageLimit