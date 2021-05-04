from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
import random
from faker import Faker
from school.models import Employees, Department, Section, Schedule, Subjects

fake = Faker()
SUBJECT_LIST_URL = reverse('api_school:admin_subject-list')


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
        rate=365,
        days_week=5,
        salary=300
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

    sched = Schedule.objects.create(
        start=fake.time(),
        end=fake.time(),
        day=random.choice(days)[0]
    )

    return sched


def section_sample():

    return Section.objects.create(name='Sample', code='Sample')


class PublicAPI(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.sched = sched_sample()
        self.sec = section_sample()
        self.school = school_sample()
        self.course = course_sample(self.school)

    def test_api_get(self):

        res = self.client.get(SUBJECT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_post(self):

        data = {
            "schedule_id": self.sched,
            "schedule": self.sched,
            "section_id": self.sec,
            "section": self.sec,
            "name": "Product Management",
            "code": "MKT - 008",
            "unit": 3,
            "lab": 0,
            "course": self.course,
        }

        res = self.client.post(SUBJECT_LIST_URL, data)
        query = Subjects.objects.all()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(query), 0)


class PrivateAPI(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.sched = sched_sample()
        self.sec = section_sample()
        self.school = school_sample()
        self.course = course_sample(self.school)
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client.force_authenticate(self.user)

    def test_api_get(self):

        res = self.client.get(SUBJECT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_post(self):

        data = {
            "schedule_id": self.sched,
            "schedule": self.sched,
            "section_id": self.sec,
            "section": self.sec,
            "name": "Product Management",
            "code": "MKT - 008",
            "unit": 3,
            "lab": 0,
            "course": self.course,
        }

        res = self.client.post(SUBJECT_LIST_URL, data)
        query = Subjects.objects.all()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(query), 0)


class SuperUserAPI(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.sched = sched_sample()
        self.sec = section_sample()
        self.school = school_sample()
        self.course = course_sample(self.school)
        self.user = get_user_model().objects.create_superuser(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client.force_authenticate(self.user)
        self.teach = teacher_sample(self.user, self.school)

    def test_api_get(self):

        res = self.client.get(SUBJECT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_post(self):

        data = {
            "name": "Product Management",
            "code": "MKT - 008",
            "unit": 3,
            "lab": 0,
            "school": self.school.id,
            "course": self.course.id,
            "cost": 200
        }

        res = self.client.post(SUBJECT_LIST_URL, data)
        query = Subjects.objects.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(query), 1)
