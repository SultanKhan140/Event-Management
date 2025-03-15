from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, RoleMst

class UserSerializer(serializers.ModelSerializer):
    """Serializer for managing users."""
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=RoleMst.objects.all(), source="role_ref", write_only=True
    )
    role_ref = serializers.CharField(source="role_ref.role_name", read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "role_ref", "role_id")

    def validate_password(self, value):
        """Hashes password before saving."""
        return make_password(value)

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Creates a new user with hashed password."""
        validated_data['role_ref_id'] = 3
        return CustomUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
