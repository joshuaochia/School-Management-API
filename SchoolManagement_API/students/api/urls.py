from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

app_name = 'api_student'

# Routers for admins to edit certain things for students
router = DefaultRouter()
router.register(
    'students',
    viewsets.StudentsViewSets,
    basename='student'
    )

# Routers for students
router.register('my-subject', viewsets.SubjectViewSet, basename='classmates')

# Urls for teacher logged in
router.register(
    'teacher/subject',
    viewsets.TeacherSubjectViewSet,
    basename='subject'
    )

urlpatterns = [
    path('', include(router.urls)),
    path('user/me', viewsets.StudentProfile.as_view())
]
