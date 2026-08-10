from rest_framework import permissions

from .models import Organization, OrganizationMembership


class IsOrganizationAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        organization_id = view.kwargs.get("pk") or view.kwargs.get("organization_pk")
        if organization_id is None:
            return True

        return OrganizationMembership.objects.filter(
            user=request.user,
            organization_id=organization_id,
            role__in=[
                OrganizationMembership.Role.OWNER,
                OrganizationMembership.Role.ADMIN,
            ],
        ).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        organization = obj if isinstance(obj, Organization) else obj.organization
        return OrganizationMembership.objects.filter(
            user=request.user,
            organization=organization,
            role__in=[
                OrganizationMembership.Role.OWNER,
                OrganizationMembership.Role.ADMIN,
            ],
        ).exists()
