from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    CODIGO = serializers.IntegerField(read_only=True)
    USUARIO = serializers.CharField(max_length=10)
    CLAVE = serializers.CharField(max_length=10)
    NOMBRE = serializers.CharField(max_length=40)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
