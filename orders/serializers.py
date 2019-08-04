from rest_framework import serializers

from orders.models import Employed, Warehouse, Order, OrderDetail


class EmployedSerializer(serializers.Serializer):
    EMPL_CO = serializers.CharField(read_only=True)
    EMPL_NO = serializers.CharField(max_length=50)
    EMPL_AP = serializers.CharField(max_length=50)

    def create(self, validate_data):
        return Employed.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.id = validate_data.get['EMPL_CO', instance.id]
        instance.first_name = validate_data.get['EMPL_NO', instance.first_name]
        instance.last_name = validate_data.get['EMPL_AP', instance.last_name]


class WarehouseSerializer(serializers.Serializer):
    CODIGO = serializers.CharField(read_only=True, max_length=10)
    DATA = serializers.CharField(read_only=True, max_length=1)
    EMPRESA = serializers.IntegerField(read_only=True)
    NOMBRE = serializers.CharField(max_length=200)

    def create(self, validate_data):
        return Warehouse.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.code = validate_data.get['CODIGO', instance.code]
        instance.data_id = validate_data.get['DATA', instance.data_id]
        instance.enterprise_id = validate_data.get['EMPRESA', instance.enterprise_id]
        instance.name = validate_data.get['NOMBRE', instance.name]


class OrderSerializer(serializers.Serializer):
    PED_ID = serializers.IntegerField(read_only=True)
    PED_FECHA = serializers.DateTimeField()
    PED_ST = serializers.CharField(max_length=5)
    PED_OBS = serializers.CharField(max_length=1000)
    PED_BOD = serializers.CharField(max_length=10)
    PED_SOL = serializers.CharField(max_length=10)

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
