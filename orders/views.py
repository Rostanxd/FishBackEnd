from django.http import HttpResponse
from django.shortcuts import render


import json


from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from orders.models import Warehouse, Employed, Order, ViewOrder
from orders.serializers import EmployedSerializer, WarehouseSerializer, OrderSerializer, ViewOrderSerializer


def index(request):
    data = {'hola': 'mundo!'}
    return HttpResponse(json.dumps(data))


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def employees_list(request):
    if request.method == 'GET':
        employees = Employed.objects.all()
        employees_serialized = EmployedSerializer(employees, many=True)
        return JSONResponse(employees_serialized.data)

    elif request.method == 'POST':
        employed_data = JSONParser().parse(request)
        employed_serialized = EmployedSerializer(data=employed_data)
        if employed_serialized.is_valid():
            employed_serialized.save()
            return JSONResponse(employed_serialized.data, status=status.HTTP_201_CREATED)
        return JSONResponse(employed_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


def employed_detail(request, pk):
    try:
        employed = Employed.objects.get(pk=pk)
    except Employed.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        employed_serialized = EmployedSerializer(employed)
        return JSONResponse(employed_serialized.data)

    elif request.method == 'PUT':
        employed_data = JSONParser().parse(request)
        employed_serializer = EmployedSerializer(employed, data=employed_data)
        if employed_serializer.is_valid():
            employed_serializer.save()
            return JSONResponse(employed_serializer.data)
        return JSONResponse(employed_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employed.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


def warehouse_list(request):
    if request.method == 'GET':
        warehouses = Warehouse.objects.all()
        warehouses_serialized = WarehouseSerializer(warehouses, many=True)
        return JSONResponse(warehouses_serialized.data)

    elif request.method == 'POST':
        warehouse_data = JSONParser().parse(request)
        warehouse_serialized = WarehouseSerializer(data=warehouse_data)
        if warehouse_serialized.is_valid():
            warehouse_serialized.save()
            return JSONResponse(warehouse_serialized.data, status=status.HTTP_201_CREATED)
        return JSONResponse(warehouse_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


def warehouse_detail(request, id, data_id, enterprise_id):
    try:
        warehouse_qs = Warehouse.objects.filter(CODIGO=id, DATA=data_id, EMPRESA=enterprise_id)
        if warehouse_qs.count() != 0:
            warehouse = warehouse_qs[0]
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except Warehouse.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        warehouse_serialized = WarehouseSerializer(warehouse)
        return JSONResponse(warehouse_serialized.data)

    elif request.method == 'POST':
        warehouse_data = JSONParser().parse(request)
        warehouse_serialized = WarehouseSerializer(warehouse, data=warehouse_data)
        if warehouse_serialized.is_valid():
            warehouse_serialized.save()
            return JSONResponse(warehouse_serialized.data)
        return JSONResponse(warehouse_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        warehouse.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


def order_list(request):
    if request.method == 'GET':
        orders = ViewOrder.objects.filter(PED_FECHA__year=2019)
        orders_serialized = ViewOrderSerializer(orders, many=True)
        return JSONResponse(orders_serialized.data)
