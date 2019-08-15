from django.http import HttpResponse

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from orders.models import Warehouse, Employed, ViewOrder, Branch, UserBranch
from orders.serializers import EmployedSerializer, WarehouseSerializer, BranchSerializer, UserBranchSerializer


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


def warehouse_list(request, name):
    if request.method == 'GET':
        warehouses = Warehouse.objects.filter(data_id__exact='O', enterprise_id__exact=1, name__icontains=name)
        warehouses_serialized = WarehouseSerializer(warehouses, many=True)
        return JSONResponse(warehouses_serialized.data)


def travel_list(request, name):
    if request.method == 'GET':
        warehouses = Warehouse.objects.filter(data_id__exact='2', enterprise_id__exact=1, name__icontains=name)
        warehouses_serialized = WarehouseSerializer(warehouses, many=True)
        return JSONResponse(warehouses_serialized.data)


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


def branch_list(request, name):
    if request.method == 'GET':
        branches = Branch.objects.filter(name__icontains=name)
        branches_serialized = BranchSerializer(branches, many=True)
        print(branches_serialized.data)
        return JSONResponse(branches_serialized.data)


def branches_by_user_list(request, user_code, branch_name):
    if request.method == 'GET':
        branches_by_user = UserBranch.objects.filter(user__code=user_code, branch__name__istartswith=branch_name,
                                                     state='A')
        branches_by_user_serialized = UserBranchSerializer(branches_by_user, many=True)
        return JSONResponse(branches_by_user_serialized.data)


def order_list(request, date_from, date_to, warehouse_id="", branch_id="", travel_id="", state="", observation="",
               provider_name=""):
    if warehouse_id is None:
        warehouse_id = ''
    if branch_id is None:
        branch_id = ''
    if travel_id is None:
        travel_id = ''
    if state is None:
        state = ''
    if observation is None:
        observation = ''
    if provider_name is None:
        provider_name = ''

    if request.method == 'GET':
        response_data = []
        vw_orders_all = ViewOrder.objects.filter(warehouse_id__icontains=warehouse_id, branch_id__icontains=branch_id,
                                                 travel_id__icontains=travel_id,
                                                 state__icontains=state, observation__icontains=observation,
                                                 # provider_name__icontains=provider_name,
                                                 date__range=(date_from, date_to)).order_by('order_id')

        vw_orders_header = vw_orders_all.values('order_id', 'date', 'observation', 'state', 'warehouse_id',
                                                'warehouse_name', 'branch_id', 'branch_name', 'travel_id',
                                                'travel_name',
                                                'applicant_id', 'applicant_name', 'provider_name').distinct()

        for header in vw_orders_header:
            vw_orders_detail = vw_orders_all.filter(order_id=header['order_id'])

            # Order detail to map
            order_detail_data = []
            for detail in vw_orders_detail:
                order_detail_data.append(
                    {'sequence': detail.detail_sequence, 'quantity': detail.detail_quantity,
                     'detail': detail.detail_detail})

            # Order header to map
            order_data = {'order_id': header['order_id'], 'date': header['date'], 'observation': header['observation'],
                          'state': header['state'], 'warehouse_id': header['warehouse_id'],
                          'warehouse_name': header['warehouse_name'], 'travel_id': header['travel_id'],
                          'travel_name': header['travel_name'],
                          'branch_id': header['branch_id'], 'branch_name': header['branch_name'],
                          'applicant_id': header['applicant_id'], 'applicant_name': header['applicant_name'],
                          'provider_name': header['provider_name'],
                          'detail': order_detail_data}

            response_data.append(order_data)

        return JSONResponse(response_data)
