from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about_page'),
    path('employees/', views.EmployeesView.as_view(), name='employees_page'),
    path('<str:slug>', views.Profile.as_view(), name='profile')

]
