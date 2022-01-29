from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'is_active', 'email', 'created_at'
        )


class RoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = (
            'id', 'name'
        )
