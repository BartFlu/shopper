from django.test import TestCase
from django.urls import reverse
from Recipes.forms import UserForm


class RegisterTestClass(TestCase):

    def test_access_by_url(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_confirm_password(self):
        form = UserForm(data={'username': 'Tester',
                              'email': 'test@test.com',
                              'password': 'Test1234test!',
                              'confirm_password': 'Test1234test'})
        self.assertFalse(form.is_valid())

    def test_confirm_password2(self):
        form = UserForm(data={'username': 'Tester',
                              'email': 'test@test.com',
                              'password': 'Test1234test!',
                              'confirm_password': 'Test1234test!'})
        self.assertTrue(form.is_valid())


class LoginTestClass(TestCase):

    def test_access_by_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_access_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

