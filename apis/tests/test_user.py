from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    User = get_user_model()

    def setUp(self):
        self.user1 = self.User.objects.create(username='user1', email='user1@github.com', password='Pa$$w0rd')
        self.user2 = self.User.objects.create(username='user2', email='user2@github.com', password='Pa$$w0rd')

    def test_get_all(self):
        url = reverse('user-get-all')
        response = self.client.get(url)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

