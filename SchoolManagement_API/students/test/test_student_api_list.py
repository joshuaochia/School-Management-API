from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
import random


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


STUDENT_URL = reverse('api_student:student-list')


class PublicStudentAPI(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()

    def test_api_get(self):

        res = self.client.get(STUDENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_post(self):

        data = {
            "id": 1,
            "user": 1,
            "school": 1,
            "course": "BSBA major in FM",
            "sex": "Male",
            "civil_status": "Married",
            "slug": "joshuacosare"
        }

        res = self.client.post(STUDENT_URL, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentAPI(TestCase):

    def setUp(self) -> None:

        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_api_get(self):

        res = self.client.get(STUDENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_post(self):

        data = {
            "user": 1,
            "school": 1,
            "sex": "Male",
            "civil_status": "Married",
            "slug": "joshuacosare"
        }

        res = self.client.post(STUDENT_URL, data)
        object = models.Students.objects.filter(**data).exists()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(object)


class StudentSuperUserAPI(TestCase):

    def setUp(self) -> None:

        self.super = get_user_model().objects.create_superuser(
            email='super@gmail.com',
            first_name='Super',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.super)
        self.school = school_sample()
        self.course = course_sample(self.school)

    def test_api_get(self):

        res = self.client.get(STUDENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_post(self):

        stats = [
            ('Married', 'Married'),
            ('Single', 'Single')
            ]

        sex = [
            ('Male', 'Male'),
            ('Female', 'Female')
            ]

        semester = [
            ('First', 'First'),
            ('Second', 'Second')
            ]

        s = random.choice(sex)[0]
        stat = random.choice(stats)[0]
        sem = random.choice(semester)[0]

        data = {
            "password": "Signup!23",
            "email": "gagokabobo@gmail.com",
            "first_name": "Taingina",
            "last_name": "shits",
            "middle_name": "fssa",
            "course_id": self.course.id,
            "school": self.school,
            "course": self.course,
            "city": "Cagayan De Oro",
            "zip_code": 9000,
            'sex': s,
            'civil_status': stat,
            'sem': sem,
            'school_yr': '2012',
        }

        res = self.client.post(STUDENT_URL, data)

        users = get_user_model().objects.all()
        user = get_user_model().objects.get(
            first_name=data['first_name'],
            last_name=data['last_name'],
            )
        object = models.Students.objects.filter(user=user).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(object)
        self.assertEqual(len(users), 2)
        self.assertTrue(user)
