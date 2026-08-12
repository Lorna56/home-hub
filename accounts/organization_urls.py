from django.urls import path
from .views import (
    OrganizationListCreateView,
    OrganizationDetailView,
    OrganizationMembershipListCreateView,
    OrganizationMembershipDetailView,
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="organizations"),
    path("<int:pk>/", OrganizationDetailView.as_view(), name="organization-detail"),
    path(
        "<int:organization_pk>/members/",
        OrganizationMembershipListCreateView.as_view(),
        name="organization-members",
    ),
    path(
        "<int:organization_pk>/members/<int:pk>/",
        OrganizationMembershipDetailView.as_view(),
        name="organization-membership-detail",
    ),
]
