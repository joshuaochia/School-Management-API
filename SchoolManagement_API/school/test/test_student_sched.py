from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .. import models
import random
from faker import Faker

SCHED_URL = reverse('api_school:admin_sched-list')
fake = Faker()

days = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ]


class PublicAPI(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_get_api(self):

        res = self.client.get(SCHED_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_api(self):

        day = random.choice(days)[0]
        data = {
            "start": fake.time(),
            "end": fake.time(),
            "day": day
        }

        res = self.client.post(SCHED_URL, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPI(TestCase):

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

    def test_get_api(self):

        res = self.client.get(SCHED_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_api(self):

        day = random.choice(days)[0]
        data = {
            "start": fake.time(),
            "end": fake.time(),
            "day": day
        }

        res = self.client.post(SCHED_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class SuperUserAPI(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_superuser(
            email='user@gmail.com',
            first_name='Normal',
            last_name='User',
            middle_name='placeholder',
            password='TestPass!23'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_api(self):

        res = self.client.get(SCHED_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_api(self):

        day = random.choice(days)[0]
        data = {
            "start": fake.time(),
            "end": fake.time(),
            "day": day
        }

        res = self.client.post(SCHED_URL, data)

        object = models.Schedule.objects.get(**data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(object)
