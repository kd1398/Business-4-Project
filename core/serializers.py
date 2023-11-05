from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import CustomUserRoles

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'is_staff']


class CustomUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserRoles
        exclude = ['user']
