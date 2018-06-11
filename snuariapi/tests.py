from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token

from snuariapi.models import *

import json

def create_user(username, password, email, name, college, major, admission_year):
    user = User.objects.create_user(username=username, password=password, email=email)
    user.profile.name = name
    user.profile.college = college
    user.profile.major = major
    user.profile.admission_year = admission_year
    return user

def login(client, user):
    token, _ = Token.objects.get_or_create(user=user)
    client.cookies['auth'] = token.key

class LoginViewTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test'
        self.user = create_user(self.username, self.password, 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_login(self):
        path = reverse('login')
        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(path=path, data=data)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['id'], self.user.id)

    def test_login_with_active_user(self):
        self.user.is_active = False
        self.user.save()

        path = reverse('login')
        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(path=path, data=data)
        self.assertEqual(response.status_code, 400)

class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = create_user('test', 'test', 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_logout(self):
        login(self.client, self.user)
        
        path = reverse('logout')

        response = self.client.post(path=path, data={})
        self.assertEqual(response.status_code, 200)

