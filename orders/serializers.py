from rest_framework import serializers

from maintenance.serializers import UserSerializer
from orders.models import Employed, Warehouse, Order, OrderDetail, ViewOrder, Branch, UserBranch


class EmployedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employed
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class UserBranchSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserBranch
        fields = '__all__'
        depth = 1


class OrderSerializer(serializers.Serializer):
    PED_ID = serializers.IntegerField(read_only=True)
    PED_FECHA = serializers.DateTimeField()
    PED_ST = serializers.CharField(max_length=5)
    PED_OBS = serializers.CharField(max_length=1000)
    # PED_BOD = serializers.CharField(max_length=10)
    PED_SOL = serializers.CharField(max_length=10)
    warehouse = serializers.StringRelatedField(many=True)

    def create(self, validate_data):
        return Order.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.id = validate_data.get['PED_ID', instance.id]
        instance.date = validate_data.get['PED_FECHA', instance.date]
        instance.state = validate_data.get['PED_ST', instance.state]
        instance.observation = validate_data.get['PED_OBS', instance.observation]


class OrderDetailSerializer(serializers.Serializer):
    PED_ID = serializers.IntegerField(read_only=True)
    PED_SEC = serializers.IntegerField(read_only=True)
    PED_CANT = serializers.IntegerField()
    PED_DETALLE = serializers.CharField(max_length=1000)

    def create(self, validate_data):
        return OrderDetail.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.sequence = validate_data.get['PED_SEC', instance.sequence]
        instance.quantity = validate_data.get['PED_CANT', instance.quantity]
        instance.detail = validate_data.get['PED_DETALLE', instance.detail]


class ViewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewOrder
        fields = '__all__'
