
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import User, Organization, OrganizationMembership
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    OrganizationSerializer,
    OrganizationMembershipSerializer,
)
from .permissions import IsOrganizationAdmin


@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


@extend_schema(tags=["Auth"])
class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["Organization"])
class OrganizationListCreateView(generics.ListCreateAPIView):

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        organization = serializer.save()
        OrganizationMembership.objects.create(
            user=self.request.user,
            organization=organization,
            role=OrganizationMembership.Role.OWNER,
        )


@extend_schema(tags=["Organization"])
class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        # Allow any authenticated user to retrieve organization details,
        # but only organization owners/admins may update or delete.
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [permissions.IsAuthenticated(), IsOrganizationAdmin()]
        return [permissions.IsAuthenticated()]


@extend_schema(tags=["Members"])
class OrganizationMembershipListCreateView(generics.ListCreateAPIView):

    serializer_class = OrganizationMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsOrganizationAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return OrganizationMembership.objects.filter(
            organization_id=self.kwargs["organization_pk"]
        )

    def perform_create(self, serializer):
        organization = Organization.objects.get(pk=self.kwargs["organization_pk"])
        serializer.save(organization=organization)


@extend_schema(tags=["Members"])
class OrganizationMembershipDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OrganizationMembershipSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationAdmin]

    def get_queryset(self):
        return OrganizationMembership.objects.filter(
            organization_id=self.kwargs["organization_pk"]
        )

