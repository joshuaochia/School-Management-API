from django.views.generic import TemplateView


class LogInView(TemplateView):

    template_name = 'login.html'


class SignUpView(TemplateView):

    template_name = 'signup.html'