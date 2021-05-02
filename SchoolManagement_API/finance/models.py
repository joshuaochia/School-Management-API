from django.db import models
from django.shortcuts import get_object_or_404
from school.models import Employees
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from students.models import StudentSubject, Students
from school.models import TeacherSubject, Employees
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
        related_name='payment'
    )
    money = models.PositiveSmallIntegerField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Student Payment')
        verbose_name_plural = _('Student Payments')


class EmployeeOT(models.Model):

    salary = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name='overtime'
    )
    hrs = models.PositiveIntegerField()
    day = models.DateField()

    class Meta:
        verbose_name = _('Employee OT')
        verbose_name_plural = _('Employee OTs')


class EmployeeLeave(models.Model):

    salary = models.ForeignKey(
        Employees,
        on_delete=models.CASCADE,
        related_name='leave'
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


@receiver(post_save, sender=EmployeeOT)
def after_overtime_created(sender, instance, created, **kwargs):

    if created:
        employee = get_object_or_404(Employees, id=instance.salary.id)
        total = (employee.rate/ 8) * instance.hrs
        employee.salary += total
        employee.save()


@receiver(post_save, sender=EmployeeLeave)
def after_leave_created(sender, instance, created, **kwargs):

    if created:
        employee = get_object_or_404(Employees, id=instance.salary.id)
        employee.salary -= employee.rate
        employee.save() 


@receiver(post_save, sender=StudentPayment)
def after_payment_created(sender, instance, created, **kwargs):

    if created:
        student = get_object_or_404(StudentBalance, id = instance.balance.id)
        student.balance -= instance.money
        student.save()

@receiver(post_save, sender=Students)
def after_student_created(sender, instance, created, **kwargs):

    if created:
        student_bal = StudentBalance.objects.create(
            student = instance
        )

        student_bal.save()

@receiver(post_save, sender=StudentSubject)
def after_add_sub(sender, instance, created, **kwargs):

    if created:
        id = instance.subject.id
        sub_teacher = get_object_or_404(TeacherSubject, id=id)
        student_bal = StudentBalance.objects.get(student=instance.student)
        cost = sub_teacher.subject.cost
        student_bal.balance += cost
        student_bal.save()