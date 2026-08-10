from rest_framework import serializers
from .models import User, Organization, OrganizationMembership


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        required=False,
    )

    class Meta:
        model = OrganizationMembership
        fields = [
            "id",
            "user",
            "organization",
            "role",
            "joined_at",
        ]
        read_only_fields = [
            "joined_at",
        ]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            **validated_data
        )

        return user