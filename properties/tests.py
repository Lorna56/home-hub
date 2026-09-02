from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User, Organization, OrganizationMembership
from .models import Property


class PropertyCreationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password123",
        )

        self.org = Organization.objects.create(name="Team Org")

    def test_user_without_organization_cannot_create_property(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("property-list-create")
        data = {
            "name": "Nice Place",
            "address": "123 Main St",
            "location": "City",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_with_organization_can_create_property(self):
        # make user a member
        OrganizationMembership.objects.create(
            user=self.user,
            organization=self.org,
            role=OrganizationMembership.Role.OWNER,
        )

        self.client.force_authenticate(user=self.user)

        url = reverse("property-list-create")
        data = {
            "name": "Nice Place",
            "address": "123 Main St",
            "location": "City",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Property.objects.filter(name="Nice Place").exists())
from django.test import TestCase

# Create your tests here.
