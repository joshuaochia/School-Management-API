from unicodedata import name
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('log-in', views.LogInView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view(), name='signup')

]