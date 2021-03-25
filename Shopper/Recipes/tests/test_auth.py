from django.test import TestCase
from django.urls import reverse


class RegisterTestClass(TestCase):

    def test_access_by_url(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class LoginTestClass(TestCase):

    def test_access_by_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
