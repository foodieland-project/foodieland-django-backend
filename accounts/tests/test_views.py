from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('accounts:create')
TOKEN_URL = reverse('accounts:token')


def create_user(**params):
    """For creating users base on params"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid data is successful"""
        data = {
            'email': 'test@amirmega.com',
            'password': 'testpass',
            'username': 'Test username'
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creatinga  user that already exists fails"""
        data = {
            'email': 'test@amirmega.com',
            'password': 'testpass',
            'username': 'Test',
        }
        create_user(**data)

        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        data = {
            'email': 'test@amirmega.com',
            'password': 'pw',
            'username': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=data['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token is created for the user"""
        data = {
            'email': 'test@amirmega.com',
            'username': 'testusername',
            'password': 'testpass',
        }
        create_user(**data)
        res = self.client.post(TOKEN_URL, data)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that the token will create with invalid credentials or not"""
        create_user(email="test@justfortest.com",
                    username="testusername", password="testpass")
        data = {
            'email': 'test@amirmega.com',
            'username': 'Test',
            'password': 'wrong',
        }

        res = self.client.post(TOKEN_URL, data)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_no_user(self):
        """Tests that token is not created for the user that doesnt exists"""
        data = {
            'email': 'test@amirmega.com',
            'password': 'testpass',
            'username': 'Test',
        }

        res = self.client.post(TOKEN_URL, data)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'none', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
