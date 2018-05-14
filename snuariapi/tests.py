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

class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = create_user('test', 'test', 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_logout(self):
        login(self.client, self.user)
        
        path = reverse('logout')

        response = self.client.post(path=path, data={})
        self.assertEqual(response.status_code, 200)

class UserSelfViewTests(TestCase):
    def setUp(self):
        self.user = create_user('test', 'test', 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_get_info(self):
        login(self.client, self.user)

        path = reverse('user_self')

        response = self.client.get(path=path)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['id'], self.user.id)

    def test_get_info_without_login(self):
        path = reverse('user_self')

        response = self.client.get(path=path)
        self.assertEqual(response.status_code, 400)

class UserDetailVeiwTests(TestCase):
    def setUp(self):
        self.user = create_user('test', 'test', 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_get_info(self):
        path = reverse('user_detail', kwargs={'pk': self.user.id})

        response = self.client.get(path=path)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['username'], self.user.username)

class ClubListViewTests(TestCase):
    def setUp(self):
        self.user = create_user('test', 'test', 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_get_club_info(self):
        path = reverse('club_list')

        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 200)

    def test_post_club(self):
        login(self.client, self.user)

        path = reverse('club_list')
        data = {
            'name': 'test club',
            'scope': '공과대학',
            'category': '봉사',
            'introduction': 'intro'
        }
        
        response = self.client.post(path=path, data=data)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result['id'])

    def test_post_club_without_login(self):
        path = reverse('club_list')
        data = {
            'name': 'test club',
            'scope': '공과대학',
            'category': '봉사',
            'introduction': 'intro'
        }
        
        response = self.client.post(path=path, data=data)
        self.assertEqual(response.status_code, 400)

class ClubDetailViewTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
                name='test club',
                scope='공과대학',
                category='봉사',
                introduction='intro'
                )
        self.user = create_user('test', 'test', 'test@test.com', 'test', '공과대학', '컴퓨터공학부', 2015)

    def test_get_club_info(self):
        path = reverse('club_detail', kwargs={'pk': self.club.id})

        response = self.client.get(path=path)
        self.assertEqual(response.status_code, 200)

    def test_edit_club_info(self):
        path = reverse('club_detail', kwargs={'pk': self.club.id})
        data = {"name": "edited name"}

        response = self.client.put(path=path, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_club(self):
        path = reverse('club_detail', kwargs={'pk': self.club.id})

        response = self.client.delete(path=path)
        self.assertEqual(response.status_code, 200)

