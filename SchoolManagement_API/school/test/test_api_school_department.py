from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
from school.api import serializers


def detail_url(school_id):

    return reverse('api_school:institution-detail', args=[school_id])


def school_department_url(school_id):

    return reverse('api_school:institution-departments', args=[school_id])


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


def department_sample(school_sample):

    department = models.Department.objects.create(
        school=school_sample,
        name='Sample'
    )

    return department


class DepartmentPublicAPI(TestCase):

    """
    TDD for end point institution-department
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
        department_sample(school)
        data = {
            'school': school,
            'name': 'sample'
        }

        url = school_department_url(school.id)

        res = self.client.get(url)
        res2 = self.client.post(url, data)

        object = models.Department.objects.filter(**data).exists()

        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(object)


class DepartmentsPrivateAPI(TestCase):

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

    def test_department_user_post_get(self):

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
            'school': school,
            'name': 'sample'
        }

        url = school_department_url(school.id)
        res = self.client.get(url)
        res2 = self.client.post(url, data)
        object = models.Department.objects.filter(**data).exists()
        query = models.Department.objects.all()
        serializer = serializers.DepartmentSerializer(query, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(object)
        self.assertNotIn(res2.data, serializer.data)


class DepartmentSuperuserAPI(TestCase):

    """
    TDD for end point institution-department with superuser
    """

    def setUp(self) -> None:

        self.user = get_user_model().objects.create_superuser(
            email='super@gmail.com',
            first_name='Super',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_department_superuser_get_post(self):

        """
        *Check if data is created when posting
        Expected result: True
        *Check the status code after posting
        Expected result: 200
        *Check the status code after get
        Expected result: 200
        """

        school = school_sample()
        data = {
            'school': school,
            'name': 'sample'
        }

        url = school_department_url(school.id)
        res = self.client.get(url)
        res2 = self.client.post(url, data)
        object = models.Department.objects.get_or_create(**data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertFalse(object[1])

    def test_department_invalid_data(self):

        """
        *Check if the model is created if there's missing data
        Expected result: False
        *Check the status code after missing some data
        Expected result: 400
        """
        school = school_sample()
        data = {
            'school': school,
            'name': '',
        }

        url = school_department_url(school.id)

        res = self.client.post(url, data)
        object = models.Department.objects.filter(**data).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(object)
