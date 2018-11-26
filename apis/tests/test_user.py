from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from faker import Faker


class UserTestCase(APITestCase):
    User = get_user_model()
    faker = Faker()

    def setUp(self):
        self.user1 = self.User.objects.create(username='user1', email='user1@github.com', password='Pa$$w0rd')
        self.user2 = self.User.objects.create(username='user2', email='user2@github.com', password='Pa$$w0rd')

    # def test_get_all(self):
    #     url = reverse('user-get-all')
    #     response = self.client.get(url)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_success(self):
        url = reverse('user-register')
        response = self.client.post(url, data={
            'username': self.faker.first_name(),
            'email': self.faker.email(),
            'password': self.faker.password()
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content_type, 'application/json')

    # def test_login(self):
    #     url = reverse('user-login')
    #     response = self.client.post(url)
    #     print(response.status_code)

