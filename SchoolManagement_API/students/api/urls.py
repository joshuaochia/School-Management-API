from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets


# Routers for admins to edit certain things for students
admin_router = DefaultRouter()
admin_router.register('list', viewsets.StudentsViewSets)
admin_router.register('subject', viewsets.SubjectViewSet)
admin_router.register('schedule', viewsets.ScheduleViewSet)

# Routers for students
user_router = DefaultRouter()
user_router.register('subjects', viewsets.GradesViewSet, basename='grades')
user_router.register('class', viewsets.ClassMateViewSet, basename='classmates')


urlpatterns = [
    path('admin/', include(admin_router.urls)),
    path('user/', include(user_router.urls)),
    path('user/me', viewsets.StudentProfile.as_view())
]
