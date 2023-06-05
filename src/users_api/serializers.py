from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        password = serializers.CharField(write_only=True, required=False)

        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name']