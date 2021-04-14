from django.db import models
from django.conf import settings

# Create your models here.


class StudentBalance(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bal'
    )
    balance = models.IntegerField(default=0)


class Payment(models.Model):
    pass


class EmployeeSalary(models.Model):
    pass
