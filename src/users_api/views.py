from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOwnerOrGetAndPostOnly, ]
