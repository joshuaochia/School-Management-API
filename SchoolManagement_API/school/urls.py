from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about_page'),
    path('employees/', views.employees, name='employees_page'),

]
