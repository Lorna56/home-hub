from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Property
from .serializers import PropertySerializer


class PropertyListCreateView(generics.ListCreateAPIView):

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(
            owner=self.request.user
        )