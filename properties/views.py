from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Property
from .serializers import PropertySerializer
from accounts.models import OrganizationMembership


class PropertyListCreateView(generics.ListCreateAPIView):

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_ids = OrganizationMembership.objects.filter(
            user=self.request.user
        ).values_list("organization_id", flat=True)

        return Property.objects.filter(
            organization_id__in=organization_ids
        )

    def perform_create(self, serializer):
        organization = serializer.validated_data["organization"]

        membership = OrganizationMembership.objects.filter(
            user=self.request.user,
            organization=organization,
            role__in=[
                OrganizationMembership.Role.OWNER,
                OrganizationMembership.Role.ADMIN,
                OrganizationMembership.Role.MANAGER,
            ]
        ).first()

        if not membership:
            raise PermissionDenied(
                "You do not have permission to create a property for this organization."
            )

        serializer.save(
            created_by=self.request.user
        )


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organization_ids = OrganizationMembership.objects.filter(
            user=self.request.user
        ).values_list("organization_id", flat=True)

        return Property.objects.filter(
            organization_id__in=organization_ids
        )