from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
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


def employees(request):
    """
    Renderer for About employees page
    """
    return render(request, 'employees.html', {})


class Profile(TemplateView, LoginRequiredMixin):

    template_name = 'profile.html'
