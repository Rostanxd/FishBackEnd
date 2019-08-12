from rest_framework import serializers

from maintenance.models import User, Role, AccessByRol


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['code', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        depth = 1


class AccessByRolSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False, read_only=True)

    class Meta:
        model = AccessByRol
        fields = ['role', 'program', 'execute', 'register', 'edit', 'delete', 'process']
        depth = 1
