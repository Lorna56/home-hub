from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserModelTests(APITestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test123@example.com",
            password="password123",
            role="TENANT",
            phone_number="0700000000",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "TENANT")
        self.assertTrue(
            user.check_password("password123")
        )


class UserRegistrationTests(APITestCase):

    def test_user_registration(self):

        url = reverse("register")

        data = {
            "username": "john",
            "email": "john123@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "role": "LANDLORD",
            "phone_number": "0700000000",
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            User.objects.count(),
            1
        )

        user = User.objects.first()

        self.assertEqual(
            user.email,
            "john@example.com"
        )


class UserListTests(APITestCase):

    def setUp(self):

        User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
            role="ADMIN",
        )


    def test_get_users(self):

        url = reverse("users")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )