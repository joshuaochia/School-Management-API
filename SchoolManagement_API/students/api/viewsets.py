from rest_framework import (
    viewsets, status, generics,
    )
from .. import models
from . import serializers, permissions as perm
from .pagination import StudentLimit
from rest_framework.decorators import action
from rest_framework.response import Response
from school.models import School
from utils import students_exception_handler as except_handler
from django.shortcuts import get_object_or_404

# viewsets for admin to facilitate students starts here

class BaseAttrViewSet(viewsets.ModelViewSet):


    def get_serializer_class(self):

        try:
            return self.serializer_class_by_action[self.action]
        except:
            return super().get_serializer_class()


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

    def filtering(self, request, querys):

        """
        Function for filtering using ?id={pk} (Feature: Update or Delete)
        The filtered model.
        """
        serializer = self.get_serializer(querys)

        if request.method == 'PUT':
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


class StudentsViewSets(BaseAttrViewSet):

    """ Viewset for creating new students with action of adding, deleting, and
        editing (Subject, section, and schedule).

        Permission: Only Admin can do this
    """

    queryset = models.Students.objects.all().order_by('-id')
    serializer_class = serializers.StudentsSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )
    pagination_class = StudentLimit

    serializer_class_by_action = {
        'subject': serializers.StudentSubjectSerializer,
    }

    def perform_create(self, serializer):
        obj = get_object_or_404(School, pk=1)
        return serializer.save(school=obj)

    @action(methods=['POST', 'GET'], detail=True, url_path='add-subject')
    def subject(self, request, pk=None):

        obj = self.get_object()
        obj_map = {
            'student': obj
        }
        try:
            query = models.StudentSubject.objects.filter(student=obj)
            serializer = self.get_serializer(query, many=True)

            self.actionhelper(request, query, obj_map)

            return Response(serializer.data)
        except:
            raise except_handler.ActionDecor()


# viewsets for admin to facilitate students ends here

# viewsets for logged in teacher ends here


class TeacherSubjectViewSet(BaseAttrViewSet):

    """
    Viewset for viewing all the subjects handled by a teacher and there's
    a feature of adding grades and absencees for each students
    """

    permission_classes = [perm.TeacherOnly, ]
    serializer_class = serializers.TeacherSubjectSerializer
    serializer_class_by_action = {
        'add_grades': serializers.TeacherStudentSerializer,
        'assignment': serializers.TeacherAssignmentSerializer,
        'project': serializers.TeacherProjectSerializer
    }

    def get_queryset(self):

        user = self.request.user
        return models.TeacherSubject.objects.filter(teacher__user=user)


    @action(detail=True, methods=['GET', 'PUT'], url_path='grades')
    def add_grades(self, request, pk=None):

        """
        endpoint for viewing all all of the student on particular subject
        and adding grades and absencees for each students
        """

        instance = self.get_object()
        try:
            user = self.request.user
            query = models.StudentSubject.objects.filter(
                subject__teacher__user=user,
                subject=instance
                )
            serializer = self.get_serializer(query, many=True)
            
            id = self.request.query_params.get('id')

            if id:
                q = get_object_or_404(
                    models.StudentSubject,
                    pk=id,
                    subject=instance
                    )
                return self.filtering(request, q)
            return Response(serializer.data)
        except:
            raise except_handler.ActionDecor()

    @action(methods=['GET', 'POST'], detail=True, url_path='assignment')
    def assignment(self, request, pk=None):

        """
        endpoint for adding new assignment for a particual subject
        and assigning it to students
        """

        obj = self.get_object()
        obj_mapping = {
            'teacher': obj
        }
        try:
            user = self.request.user
            query = models.Assignment.objects.filter(
                subject__teacher__user=user,
                subject=obj
                )
            serializer = self.get_serializer(query, many=True)

            id = self.request.query_params.get('id')

            if id:
                q = get_object_or_404(
                    models.Assignment,
                    pk=id,
                    subject=obj
                    )
                return self.filtering(request, q)

            self.actionhelper(request, query, obj_mapping)

            return Response(serializer.data)
        except:
            raise except_handler.ActionDecor()

    @action(methods=['GET', 'PUT', 'POST'], detail=True, url_path='project')
    def project(self, request, pk=None):

        """
        endpoint for adding new project for a particual subject
        and assigning it to students
        """
        
        obj = self.get_object()
        obj_mapping = {
            'teacher': obj
        }
        try:
            user = self.request.user
            query = models.Project.objects.filter(
            subject__teacher__user=user,
            subject=obj
                )
            serializer = self.get_serializer(query, many=True)

            id = self.request.query_params.get('id')

            if id:
                q = get_object_or_404(
                    models.Project,
                    pk=id,
                    subject=obj
                    )
                return self.filtering(request, q)

            self.actionhelper(request, query, obj_mapping)

            return Response(serializer.data)

        except:
            raise except_handler.ActionDecor()

# viewsets for logged in teacher ends here

# viewsets for logged in student starts here


class StudentProfile(generics.RetrieveUpdateDestroyAPIView):

    """
    Viewsset for viewing or updating the curret logged in student profile
    """

    serializer_class = serializers.StudentOwnerSerializer

    def get_object(self):
        return get_object_or_404(models.Students, user=self.request.user)


class SubjectViewSet(BaseAttrViewSet):

    """
    Viewset for viewing all subjects of current student
    """

    serializer_class = serializers.StudentSubjectSerializer
    permission_classes = (perm.IsAdminUserOrReadOnly, )

    serializer_class_by_action = {
        'list': serializers.ClassMateSerializer,
        'classmates': serializers.StudentOwnerSerializer,
        'assignments': serializers.StudentAssignmentSerializer,
        'projects': serializers.StudentProjectSerializer
    }

    def get_queryset(self):

        user = self.request.user
        query = models.StudentSubject.objects.filter(student__user=user)
        return query


    @action(methods=['GET', ], detail=True, url_path='classmates')
    def classmates(self, request, pk=None):

        """
        This viewset is for viewing classmates for a specific subject
        """

        obj = self.get_object().subject
        try:
            query = models.Students.objects.filter(student_sub__subject=obj)
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data)
        except:
            raise except_handler.ActionDecor()

    @action(methods=['GET', 'PUT'], detail=True, url_path='assignments')
    def assignments(self, request, pk=None):

        """
        This viewset is for viewing assignments for a specific subject
        and passing the file required for the assignment
        """

        obj = self.get_object()
        try:
            queryset = models.Assignment.objects.filter(
                subject=obj.subject,
                assign=obj
                )
            serializer = self.get_serializer(queryset, many=True)

            id = self.request.query_params.get('id')

            if id:
                query = get_object_or_404(
                    models.Assignment,
                    id=id,
                    assign=obj
                    )
                return self.filtering(request, query)

            return Response(serializer.data)
        except:
            raise except_handler.ActionDecor()

    @action(methods=['GET', 'PUT'], detail=True, url_path='projects')
    def projects(self, request, pk=None):

        """
        This viewset is for viewing projects for a specific subject
        and passing the file required for the project
        """

        obj = self.get_object()
        try:
            query = models.Project.objects.filter(
                subject=obj.subject,
                assign=obj
                )
            serializer = self.get_serializer(query, many=True)

            id = self.request.query_params.get('id')

            if id:
                query = get_object_or_404(
                    models.Project,
                    id=id,
                    assign=obj
                    )
                return self.filtering(request, query)

            return Response(serializer.data)
        except:
            raise except_handler.ActionDecor()

# viewsets for logged in student ends here
