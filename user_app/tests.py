from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your tests here.

class RegisterTestCase(APITestCase):
    def test_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        
class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'superman', password = 'vizag@123')
        
    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'superman',
            'password': 'vizag@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
    def test_logout(self):
        url = reverse('logout')
        self.token = Token.objects.get(user__username = 'superman')
        self.client.credentials(HTTP_AUTHORIZATION = 'Token '+ self.token.key)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)