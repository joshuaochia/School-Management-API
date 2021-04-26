from django.db import models
from django.conf import settings
from students.models import Students
from school.models import Employees
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class StudentBalance(models.Model):

    student = models.OneToOneField(
        Students,
        on_delete=models.CASCADE,
        related_name='bal'
    )
    balance = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Student Balance')
        verbose_name_plural = _('Student Balances')


class StudentPayment(models.Model):

    balance = models.ForeignKey(
        StudentBalance,
        on_delete=models.CASCADE,
        related_name='student_balance'
    )
    money = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = _('Student Payment')
        verbose_name_plural = _('Student Payments')

class EmployeeSalary(models.Model):

    employee = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name='employee_salary'
    )
    rate = models.PositiveSmallIntegerField(verbose_name='Daily Rate')
    week_hrs = models.PositiveSmallIntegerField(verbose_name='Weekly Hrs')
    salary = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Employee Salary')
        verbose_name_plural = _('Employee Salaries')


class EmployeeOT(models.Model):

    salary = models.ForeignKey(
        EmployeeSalary,
        on_delete=models.CASCADE,
    )
    hrs = models.PositiveIntegerField()
    day = models.DateField()

    class Meta:
        verbose_name = _('Employee OT')
        verbose_name_plural = _('Employee OTs')

class EmployeeLeave(models.Model):

    salary = models.ForeignKey(
        EmployeeSalary,
        on_delete=models.CASCADE,
    )
    day = models.DateField()

    class Meta:
        verbose_name = _('Employee Leave')
        verbose_name_plural = _('Employee Leaves')


class SchoolPayedHolidays(models.Model):

    name = models.CharField(max_length=255)
    date = models.DateField()


    class Meta:
        verbose_name = _('School Holiday')
        verbose_name_plural = _('School Holidays')
