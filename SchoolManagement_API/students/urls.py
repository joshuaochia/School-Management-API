from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('schedule', views.ScheduleView.as_view(), name='schedule'),
    path('subject', views.StudentSubject.as_view(), name='subject'),
    path('balance', views.StudentBalance.as_view(), name='balance')
]