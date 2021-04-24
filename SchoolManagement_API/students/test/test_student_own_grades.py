from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from faker import Faker
from .. import models
from school.models import Employees, Department
import random

fake = Faker()


def teacher_sample(user, school, ):

    department = Department.objects.create(
        school=school,
        name='Sample'
    )
    emp = Employees.objects.create(
        created_by=user,
        user=user,
        school=school,
        department=department,
    )

    return emp


def school_sample():

    school = models.School.objects.create(
        name='Test School',
        vision='Test Vision',
        mission='Test Mission',
        street='Test Street',
        city='Test City',
        zip_code='900'
    )

    return school


def course_sample(school_sample):

    course = models.Courses.objects.create(
        school=school_sample,
        course='Bachelor of Science in Business',
        major='Marketing'
    )

    return course


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

    sched = models.Schedule.objects.create(
        start=fake.time(),
        end=fake.time(),
        day=random.choice(days)[0]
    )

    return sched


def section_sample():

    return models.Section.objects.create(name='Sample', code='Sample')


def subject_sample(sample_course):

    sec = section_sample()
    sched = sched_sample()
    sub = models.Subjects.objects.create(
        name='TEST SUB',
        teacher=None,
        course=sample_course,
        unit=0,
        lab=0,
        section=sec,
        schedule=sched
    )

    return sub


def student_sample(user, school, course):

    stud = models.Students.objects.create(
        user=user,
        school=school,
        course=course
    )

    return stud


URL = reverse('api_student:grades-list')


class PublicAPI(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()

    def test_get_api(self):

        res = self.client.get(URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPI(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.school = school_sample()
        self.client.force_authenticate(self.user)
        self.course = course_sample(self.school)
        self.subject = subject_sample(self.course)
        self.student = student_sample(self.user, self.school, self.course)

        self.stud_sub = models.StudentSubject.objects.create(
            student=self.student,
            subject=self.subject
        )

    def test_get_api(self):

        res = self.client.get(URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
