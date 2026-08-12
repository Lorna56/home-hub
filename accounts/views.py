
from rest_framework import generics, permissions
from .models import User, Organization, OrganizationMembership
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    OrganizationSerializer,
    OrganizationMembershipSerializer,
)
from .permissions import IsOrganizationAdmin


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


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


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        # Allow any authenticated user to retrieve organization details,
        # but only organization owners/admins may update or delete.
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [permissions.IsAuthenticated(), IsOrganizationAdmin()]
        return [permissions.IsAuthenticated()]


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


class OrganizationMembershipDetailView(generics.DestroyAPIView):

    serializer_class = OrganizationMembershipSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationAdmin]

    def get_queryset(self):
        return OrganizationMembership.objects.filter(
            organization_id=self.kwargs["organization_pk"]
        )

