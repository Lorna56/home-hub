from django.urls import path
from .views import (
    RegisterView,
    UserListView,
    OrganizationListCreateView,
    OrganizationDetailView,
    OrganizationMembershipListCreateView,
    OrganizationMembershipDetailView,
)


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "users/",
        UserListView.as_view(),
        name="users",
    ),

    path(
        "organizations/",
        OrganizationListCreateView.as_view(),
        name="organizations",
    ),

    path(
        "organizations/<int:pk>/",
        OrganizationDetailView.as_view(),
        name="organization-detail",
    ),

    path(
        "organizations/<int:organization_pk>/members/",
        OrganizationMembershipListCreateView.as_view(),
        name="organization-members",
    ),

    path(
        "organizations/<int:organization_pk>/members/<int:pk>/",
        OrganizationMembershipDetailView.as_view(),
        name="organization-membership-detail",
    ),
]