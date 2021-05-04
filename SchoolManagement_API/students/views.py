from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ScheduleView(TemplateView, LoginRequiredMixin):

    template_name = 'schedule.html'


class StudentBalance(TemplateView, LoginRequiredMixin):

    template_name = 'balance.html'


class StudentSubject(TemplateView, LoginRequiredMixin):

    template_name = 'subject.html'