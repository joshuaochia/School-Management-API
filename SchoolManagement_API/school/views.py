from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    """
    Renderer for Home Page
    """
    try:
        school = models.School.objects.get(id=1)
    except models.School.DoesNotExist:
        raise Http404

    context = {
        'school': school
    }

    return render(request, 'index.html', context)


def about(request):
    """
    Renderer for About Page
    """
    try:
        school = models.School.objects.values_list('id' ,'vision', 'mission',).get(id=1)
    except models.School.DoesNotExist:
        raise Http404

    context = {
        'school': school
    }

    return render(request, 'about.html', context)


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
