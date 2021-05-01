from school.test.test_api_school_department import department_sample
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
from students.models import Students
from school.models import (
    Courses, School, Schedule, Section, TeacherSubject, Subjects, Employees
    )
from faker import Faker
import random

fake = Faker()


def sched_sample():

    days = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ]

    sched = Schedule.objects.create(
        start=fake.time(),
        end=fake.time(),
        day=random.choice(days)[0]
    )

    return sched

def section_sample():

    return Section.objects.create(name='Sample', code='Sample')


def subject_sample(sample_course, school):

    sub = Subjects.objects.create(
        name='TEST SUB',
        course=sample_course,
        unit=0,
        lab=0,
        cost = 200,
        school = school
    )

    return sub

def teacher_sub_sample(subject, schedule, section):

    teach_sub = TeacherSubject.objects.create(
        subject=subject,
        schedule=schedule,
        section=section
    )

    return teach_sub


def sample_students(school, course): 


    user = get_user_model().objects.create_user(
        email='Test@gmail.com',
        password='TestPass',
        first_name='Test',
        last_name='User',
        middle_name='Test',
    )
    student = Students.objects.create(
        user=user,
        school=school,
        course=course,
    )

    return student

def school_sample():

    school = School.objects.create(
        name='Test School',
        vision='Test Vision',
        mission='Test Mission',
        street='Test Street',
        city='Test City',
        zip_code='900'
    )

    return school


def course_sample(school_sample):

    course = Courses.objects.create(
        school=school_sample,
        course='Bachelor of Science in Business',
        major='Marketing'
    )

    return course

class StudentBalanceTest(TestCase):

    def setUp(self) -> None:

        self.client = Client()
    
        self.school = school_sample()
        self.course = course_sample(self.school)
        self.student = sample_students(self.school, self.course)
        self.sub = subject_sample(self.course, self.school)
        self.sched = sched_sample()
        self.section = section_sample()
        self.teach_sub = teacher_sub_sample(
            subject=self.sub,
            schedule=self.sched,
            section=self.section
        )

    def test_student_signal(self):

        all_balance = models.StudentBalance.objects.all()

        self.assertEqual(len(all_balance), 1)
        self.assertIn(self.student.bal, all_balance)


    def test_student_payment(self):

        self.student.bal.balance = 3000
        self.student.bal.save()

        payment= models.StudentPayment.objects.create(
            balance = self.student.bal,
            money = 200
        )
        all_payments = models.StudentPayment.objects.all()
        self.student.bal.refresh_from_db()
        
    

        self.assertEqual(len(all_payments), 1)
        self.assertEqual(self.student.bal.balance, 2800)

    def test_student_add_sub(self):

        self.student.bal.balance = 0
        self.student.bal.save()
        student_sub = models.StudentSubject.objects.create(
            student = self.student,
            subject = self.teach_sub
        )
        self.student.bal.refresh_from_db()

        self.assertEqual(self.student.bal.balance, 200)


class EmployeeSalaryTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.created_by = get_user_model().objects.create_superuser(
            email='created.by@gmail.com',
            first_name='created',
            last_name='User',
            middle_name='By',
            password='TestPass!23'
        )
        self.school = school_sample()
        self.department = department_sample(self.school)
        self.employee = Employees.objects.create(
            created_by=self.created_by,
            user=self.user,
            school=self.school,
            department=self.department,
            rate=365,
            days_week=5,
            salary=5000
        )

    def test_employee_leave(self):

        emp_ot = models.EmployeeOT.objects.create(
            salary=self.employee,
            hrs=2,
            day=fake.date()
        )
        all_ot = models.EmployeeOT.objects.all()
        self.assertEqual(len(all_ot), 1)

        emp_ot.salary.refresh_from_db()

        total = int(5000 + (365/8) * 2)

        # emp = Employees.refresh_from_db()

        self.assertEqual(self.employee.salary, total)

    def test_employee_ot(self):

        emp_leave = models.EmployeeLeave.objects.create(
            salary=self.employee,
            day=fake.date()
        )

        emp_leave.salary.refresh_from_db()

        self.assertEqual(self.employee.salary, 4635)