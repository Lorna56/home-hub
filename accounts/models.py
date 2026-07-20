from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        LANDLORD = "LANDLORD", "Landlord"
        TENANT = "TENANT", "Tenant"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TENANT
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username