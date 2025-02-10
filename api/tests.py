from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
import jwt
import datetime
from django.conf import settings

class AuthTests(APITestCase):
    def generate_jwt(self, email, name, picture=None):
        payload = {
            'email': email,
            'name': name,
            'picture': picture,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        }
        return jwt.encode(payload, settings.JWT_DECODE_KEY, algorithm='HS256')

    def test_register_new_user(self):
        url = reverse('register')
        jwt_token = self.generate_jwt('newuser@example.com', 'New User', 'http://example.com/image.jpg')
        data = {'token': jwt_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_existing_user(self):
        # First register a user
        self.test_register_new_user()
        url = reverse('login')
        jwt_token = self.generate_jwt('newuser@example.com', 'New User', 'http://example.com/image.jpg')
        data = {'token': jwt_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        # First register and login
        register_url = reverse('register')
        jwt_token = self.generate_jwt('testuser@example.com', 'Test User')
        register_data = {'token': jwt_token}
        register_response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_url = reverse('login')
        login_data = {'token': jwt_token}
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data['access']

        # Now get user detail
        user_detail_url = reverse('user-detail')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        user_detail_response = self.client.get(user_detail_url, format='json')
        self.assertEqual(user_detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_detail_response.data['email'], 'testuser@example.com')