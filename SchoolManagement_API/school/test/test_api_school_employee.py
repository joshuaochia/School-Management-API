from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
from school.api import serializers


EMP_URL = reverse('api_school:employees-list')


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


class EmployeePublicAPI(TestCase):

    """
    TDD for employees-list
    """

    def setUp(self):

        self.client = APIClient()
        self.school = school_sample()
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
        self.department = department_sample(self.school)

    def test_school_employees_get_post(self):

        """
        * Check for getting the API if not authorized
        Expected result: 200
        * Check for posting with no authentication
        Expected result: 401
        * Check if the data posted is not created
        Excpected result: False
        """

        data = {
            'created_by': self.created_by,
            'user': self.user,
            'school': self.school,
            'department': self.department,
            'position': 'Teacher',
        }

        res = self.client.get(EMP_URL)
        res2 = self.client.post(EMP_URL, data)

        object = models.Employees.objects.filter(**data).exists()

        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(object)


class EmployeePrivateAPI(TestCase):

    """
    TDD for end point employee with user authenticated
    """

    def setUp(self):

        self.school = school_sample()
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
        self.department = department_sample(self.school)
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

        data = {
            "position": "Department Head",
            "bday": "2017-08-20",
            "country": "PH",
            "city": "Paulbury",
            "zip_code": 900,
            "sex": "Female",
            "civil_status": "Single",
            "slug": "kyleburton",
            "user": self.user,
            "school": self.school,
            "department": self.department,
            'created_by': self.created_by,
        }

        res = self.client.get(EMP_URL)
        res2 = self.client.post(EMP_URL, data)

        object = models.Employees.objects.filter(**data).exists()
        query = models.Employees.objects.all()

        serializer = serializers.EmployeesSerializer(query, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(object)
        self.assertNotIn(res2.data, serializer.data)
