
from rest_framework import generics
from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

# Create your views here.
