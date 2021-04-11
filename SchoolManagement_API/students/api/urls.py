from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets

admin_router = DefaultRouter()
admin_router.register('list', viewsets.StudentsViewSets)
admin_router.register('subject', viewsets.SubjectViewSet)
admin_router.register('schedule', viewsets.ScheduleViewSet)
admin_router.register('section', viewsets.SectionViewSet)

user_router = DefaultRouter()

user_router.register('subjects', viewsets.GradesViewSet, basename='users2')


urlpatterns = [
    path('admin/', include(admin_router.urls)),
    path('user/', include(user_router.urls)),
    path('user/me', viewsets.StudentProfile.as_view())
]
