from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models


SCHOOl_URL = reverse('api_school:institution-list')


class PublicAPISchool(TestCase):

    """
    TDD for api institution-list with no authentication
    """

    def setUp(self):

        self.client = APIClient()

    def test_api_avail(self):

        """
        *Check the status code of get
        Expected result: 200
        """
        res = self.client.get(SCHOOl_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_posting_not_admin(self):

        """
        *Check the status of post for creating a new school
        Expected result: 401
        *Check if the data is created after posting
        Expected result: False
        """
        data = {
            'name': 'COC 2',
            'vision': 'New_vision',
            'mission': 'new_mission',
            'street': 'new_Street',
            'country': 'Philppines',
            'city': 'New_city',
            'zip_code': '9010'
            }

        res = self.client.post(SCHOOl_URL, data)
        object = models.School.objects.filter(**data).exists()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(object)


class PrivateApiSchool(TestCase):

    """
    TDD for api institution-list with authentication of superuser or user
    """

    def setUp(self):

        self.super_user = get_user_model().objects.create_superuser(
            email='super@gmail.com',
            first_name='Super',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )

        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )

        self.data = {
            'name': 'COC 2',
            'vision': 'New_vision',
            'mission': 'new_mission',
            'street': 'new_Street',
            'city': 'New_city',
            'zip_code': '9010'
            }
        self.client = APIClient()

    def test_posting_for_superuser(self):
        """
        *Check post method status code
        Expected result: 201
        *Check if the data is created after the post
        Expected result: True
        """

        self.client.force_authenticate(self.super_user)

        res = self.client.post(SCHOOl_URL, self.data)

        object = models.School.objects.get(**self.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(object)

    def test_posting_for_user(self):

        """
        *Check post method status code
        Expected result: 401
        *Check if the data is created after the post
        Expected result: False
        """

        res = self.client.post(SCHOOl_URL, self.data)

        object = models.School.objects.filter(**self.data).exists()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(object)
