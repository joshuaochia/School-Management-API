from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

app_name = 'api_student'

# Routers for admins to edit certain things for students
admin_router = DefaultRouter()
admin_router.register(
    'list',
    viewsets.StudentsViewSets,
    basename='student'
    )
admin_router.register(
    'subject',
    viewsets.SubjectViewSet,
    basename='admin_subject'
    )
admin_router.register(
    'schedule',
    viewsets.ScheduleViewSet,
    basename='admin_sched'
    )

# Routers for students
user_router = DefaultRouter()
user_router.register('subjects', viewsets.GradesViewSet, basename='grades')
user_router.register('class', viewsets.ClassMateViewSet, basename='classmates')

# Urls for teacher logged in
user_router.register(
    'teacher/subject',
    viewsets.TeacherSubjectViewSet,
    basename='subject'
    )

urlpatterns = [
    path('admin/', include(admin_router.urls)),
    path('user/', include(user_router.urls)),
    path('user/me', viewsets.StudentProfile.as_view())
]
