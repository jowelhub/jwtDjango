from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'profile_image']

class FrontendJWTSerializer(serializers.Serializer):
    token = serializers.CharField()
