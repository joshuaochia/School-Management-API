from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
from school.api import serializers


def detail_url(school_id):

    return reverse('api_school:institution-detail', args=[school_id])


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


def policy_sample(school_sample):

    policy = models.Policies.objects.create(
        school=school_sample,
        policy='Sample'
    )

    return policy


def school_policy_url(school_id):

    return reverse('api_school:institution-policies', args=[school_id])


class PoliciesPublicAPI(TestCase):

    """
    TDD for end point institution-policies and institution-detail
    """

    def setUp(self) -> None:

        self.client = APIClient()

    def test_school_detail(self):

        """
        *Check for getting a detail view with no authentication
        Expected result: 200
        """
        school = school_sample()

        url = detail_url(school.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_school_policies_get_post(self):

        """
        * Check for getting the API if not authorized
        Expected result: 200
        * Check for posting with no authentication
        Expected result: 401
        * Check if the data posted is not created
        Excpected result: False
        """

        school = school_sample()
        policy_sample(school)
        data = {
            'school': school,
            'policy': 'sample'
        }

        url = school_policy_url(school.id)
        res = self.client.get(url)

        res2 = self.client.post(url, data)
        object = models.Policies.objects.filter(**data).exists()

        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(object)


class PoliciesPrivateAPI(TestCase):

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

    def test_policy_user_post_get(self):

        """
        *Check if the get method is avail if user authenticated
        Expected result: 200
        *Check if the status code for posting with authenticated user
        Expected result: 403
        *Check if the model is created after posting
        Expected result: False
        """

        school = school_sample()
        data = {
            'school': school,
            'policy': 'sample'
        }

        url = school_policy_url(school.id)
        res = self.client.get(url)

        res2 = self.client.post(url, data)
        object = models.Policies.objects.filter(**data).exists()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(object)


class PolicySuperuserAPI(TestCase):

    """
    TDD for end point institution-policies if superuser
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

    def test_policy_superuser_get_post(self):

        """
        *Check the get method
        Expected result: 200
        *Check the post status code if superuser
        Expected result: 200
        *Check if the data existed after posting
        Expected result: True or 1 == 1
        *Check the filter 'id' and if it's get the equal data
        Expected result: True
        """

        school = school_sample()
        data = {
            'school': school,
            'policy': 'sample'
        }

        url = school_policy_url(school.id)
        res = self.client.get(url)
        res2 = self.client.post(url, data)

        object = models.Policies.objects.get(**data)

        res3 = self.client.get(url, {'id': f'{object.id}'})

        query = models.Policies.objects.all()
        serializer = serializers.PoliciesSerializer(object)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertIn(object, query)
        self.assertEqual(len(query), 1)
        self.assertEqual(serializer.data, res3.data)
