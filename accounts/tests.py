from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    User,
    Organization,
    OrganizationMembership,
)


class UserModelTests(APITestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            phone_number="0700000000",
        )

        self.assertEqual(user.username, "testuser")
        self.assertTrue(
            user.check_password("password123")
        )


class UserRegistrationTests(APITestCase):

    def test_user_registration(self):

        url = reverse("register")

        data = {
            "username": "john",
            "email": "john88@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
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
            "john88@example.com"
        )


class UserListTests(APITestCase):

    def setUp(self):

        User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
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


class OrganizationTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )
        self.client.force_authenticate(user=self.owner)

    def test_create_organization_assigns_owner_membership(self):
        url = reverse("organizations")
        response = self.client.post(
            url,
            {"name": "Test Organization"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.get(name="Test Organization")
        self.assertTrue(
            OrganizationMembership.objects.filter(
                user=self.owner,
                organization=organization,
                role=OrganizationMembership.Role.OWNER,
            ).exists()
        )

    def test_owner_can_add_member(self):
        organization = Organization.objects.create(name="Team Org")
        OrganizationMembership.objects.create(
            user=self.owner,
            organization=organization,
            role=OrganizationMembership.Role.OWNER,
        )

        member = User.objects.create_user(
            username="tenant",
            email="tenant@example.com",
            password="password123",
        )

        url = reverse(
            "organization-members",
            kwargs={"organization_pk": organization.pk},
        )

        response = self.client.post(
            url,
            {
                "user": member.pk,
                "role": OrganizationMembership.Role.TENANT,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            OrganizationMembership.objects.filter(
                user=member,
                organization=organization,
                role=OrganizationMembership.Role.TENANT,
            ).exists()
        )

    def test_non_admin_cannot_add_member(self):
        organization = Organization.objects.create(name="Team Org")
        non_admin = User.objects.create_user(
            username="nonadmin",
            email="nonadmin@example.com",
            password="password123",
        )
        OrganizationMembership.objects.create(
            user=non_admin,
            organization=organization,
            role=OrganizationMembership.Role.TENANT,
        )

        self.client.force_authenticate(user=non_admin)
        new_member = User.objects.create_user(
            username="newuser",
            email="newuser@example.com",
            password="password123",
        )

        url = reverse(
            "organization-members",
            kwargs={"organization_pk": organization.pk},
        )

        response = self.client.post(
            url,
            {
                "user": new_member.pk,
                "role": OrganizationMembership.Role.TENANT,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_remove_member(self):
        organization = Organization.objects.create(name="Team Org")
        OrganizationMembership.objects.create(
            user=self.owner,
            organization=organization,
            role=OrganizationMembership.Role.OWNER,
        )
        member = User.objects.create_user(
            username="tenant",
            email="tenant@example.com",
            password="password123",
        )
        membership = OrganizationMembership.objects.create(
            user=member,
            organization=organization,
            role=OrganizationMembership.Role.TENANT,
        )

        url = reverse(
            "organization-membership-detail",
            kwargs={
                "organization_pk": organization.pk,
                "pk": membership.pk,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            OrganizationMembership.objects.filter(pk=membership.pk).exists()
        )

    def test_owner_can_update_organization(self):
        organization = Organization.objects.create(name="Team Org")
        OrganizationMembership.objects.create(
            user=self.owner,
            organization=organization,
            role=OrganizationMembership.Role.OWNER,
        )

        url = reverse("organization-detail", kwargs={"pk": organization.pk})

        response = self.client.patch(
            url,
            {"name": "Updated Org"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization.refresh_from_db()
        self.assertEqual(organization.name, "Updated Org")

    def test_non_admin_cannot_update_organization(self):
        organization = Organization.objects.create(name="Team Org")
        non_admin = User.objects.create_user(
            username="nonadmin",
            email="nonadmin2@example.com",
            password="password123",
        )
        OrganizationMembership.objects.create(
            user=non_admin,
            organization=organization,
            role=OrganizationMembership.Role.TENANT,
        )

        self.client.force_authenticate(user=non_admin)

        url = reverse("organization-detail", kwargs={"pk": organization.pk})

        response = self.client.patch(
            url,
            {"name": "Malicious Update"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_organization(self):
        organization = Organization.objects.create(name="Team Org")
        OrganizationMembership.objects.create(
            user=self.owner,
            organization=organization,
            role=OrganizationMembership.Role.OWNER,
        )

        url = reverse("organization-detail", kwargs={"pk": organization.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Organization.objects.filter(pk=organization.pk).exists())

    def test_non_admin_cannot_delete_organization(self):
        organization = Organization.objects.create(name="Team Org")
        non_admin = User.objects.create_user(
            username="nonadmin2",
            email="nonadmin3@example.com",
            password="password123",
        )
        OrganizationMembership.objects.create(
            user=non_admin,
            organization=organization,
            role=OrganizationMembership.Role.TENANT,
        )

        self.client.force_authenticate(user=non_admin)

        url = reverse("organization-detail", kwargs={"pk": organization.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
