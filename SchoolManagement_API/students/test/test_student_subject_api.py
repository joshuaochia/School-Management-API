from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models

import random
from faker import Faker

fake = Faker()


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


def student_sample(school_sample, course_sample):

    user = get_user_model().objects.create_user(
        email='sample@gmail.com',
        first_name='First',
        last_name='Last',
        middle_name='Middle',
        password='TestPass!23'
    )
    student = models.Students.objects.create(
        user=user,
        school=school_sample,
        course=course_sample
    )

    return student


def subject_url(student_id):

    return reverse('api_student:student-subject', args=[student_id])


class PublicAPI(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.school = school_sample()
        self.course = course_sample(self.school)
        self.student = student_sample(self.school, self.course)

    def test_get_api(self):

        url = subject_url(self.student.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_api(self):

        url = subject_url(self.student.id)
        sub = subject_sample(self.course)
        data = {
            'subject_id': sub.id
        }

        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPI(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.school = school_sample()
        self.course = course_sample(self.school)
        self.student = student_sample(self.school, self.course)
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client.force_authenticate(self.user)

    def test_get_api(self):

        url = subject_url(self.student.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_api(self):

        url = subject_url(self.student.id)
        sub = subject_sample(self.course)
        data = {
            'subject_id': sub.id
        }

        res = self.client.post(url, data)

        query = models.StudentSubject.objects.all()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(query), 0)


class SuperUser(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.school = school_sample()
        self.course = course_sample(self.school)
        self.student = student_sample(self.school, self.course)
        self.user = get_user_model().objects.create_superuser(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client.force_authenticate(self.user)

    def test_post_api(self):

        url = subject_url(self.student.id)
        sub = subject_sample(self.course)
        data = {
            'subject_id': sub.id
        }

        res = self.client.post(url, data)
        query = models.StudentSubject.objects.all()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(query), 1)
