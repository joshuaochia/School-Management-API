from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
from school.api import serializers
from ..conf import courses, majors
import random


def school_course_url(school_id):

    return reverse('api_school:institution-courses', args=[school_id])


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


class CoursePublicAPI(TestCase):

    """
    TDD for end point institution-courses
    """

    def setUp(self):

        self.client = APIClient()

    def test_school_departments_get_post(self):

        """
        * Check for getting the API if not authorized
        Expected result: 200
        * Check for posting with no authentication
        Expected result: 401
        * Check if the data posted is not created
        Excpected result: False
        """

        school = school_sample()
        data = {
            'school': school,
            'major': 'Marketing',
            'course': 'Bachelor of Science in Business'
        }

        url = school_course_url(school.id)

        res = self.client.get(url)
        res2 = self.client.post(url, data)

        object = models.Courses.objects.filter(**data).exists()

        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(object)


class CoursePrivateAPI(TestCase):

    """
    TDD for end point institution-department with user authenticated
    """

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_course_user_post_get(self):

        """
        *Check if the get method is avail if user authenticated
        Expected result: 200
        *Check if the status code for posting with authenticated user
        Expected result: 403
        *Check if the model is created after posting
        Expected result: False
        *Chech if the data post data not in serializer
        Expected result: True
        """

        school = school_sample()
        data = {
            "course": "Bachelor of Science in Business",
            "major": "Marketing",
            "school": school
        }

        url = school_course_url(school.id)
        res = self.client.get(url)
        res2 = self.client.post(url, data)

        object = models.Courses.objects.filter(**data).exists()
        query = models.Courses.objects.all()

        serializer = serializers.DepartmentSerializer(query, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(object)
        self.assertNotIn(res2.data, serializer.data)


class CourseSuperuserAPI(TestCase):

    """
    TDD for end point institution-department with superuser
    """

    def setUp(self):

        self.user = get_user_model().objects.create_superuser(
            email='ochia@gmail.com',
            first_name='Testsssss',
            middle_name='Middlesss',
            last_name='Supersss',
            password='Signup!23'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_course_superuser_get_post(self):

        """
        *Check if data is created when posting
        Expected result: True
        *Check the status code after posting
        Expected result: 200
        *Check the status code after get
        Expected result: 200
        """
        major1 = random.choice(majors)[0]
        course1 = random.choice(courses)[0]
        school = school_sample()
        data = {
            "course": course1,
            "major": major1,
            "school": school,
        }

        url = school_course_url(school.id)

        res = self.client.post(url, data)
        object = models.Courses.objects.get_or_create(**data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(object[1])

    def test_course_invalid_data(self):

        """
        *Check if the model is created if there's missing data
        Expected result: False
        *Check the status code after missing some data
        Expected result: 400
        """
        school = school_sample()
        data = {
            'school': school,
            'major': '',
            'course': ''
        }

        url = school_course_url(school.id)

        res = self.client.post(url, data)
        object = models.Courses.objects.filter(**data).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(object)
