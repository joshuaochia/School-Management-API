from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    """
    Renderer for Home Page
    """
    return render(request, 'index.html', {})


def about(request):
    """
    Renderer for About Page
    """
    return render(request, 'about.html', {})


class EmployeesView(ListView, LoginRequiredMixin):

    template_name = 'employees.html'
    model = models.Employees
    context_object_name = 'employees'


class Profile(DetailView, LoginRequiredMixin):

    template_name = 'profile.html'
    model = models.Employees
    context_object_name = 'employees_detail'

    def get_object(self):
        return get_object_or_404(models.Employees, slug=self.kwargs.get('slug'))
