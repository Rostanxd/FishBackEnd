import json

from django.db.models.functions import Concat
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from orders.models import Warehouse, Employed, ViewOrder, Branch, UserBranch, Order, OrderDetail
from orders.serializers import EmployedSerializer, WarehouseSerializer, BranchSerializer, UserBranchSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def employees_list(request, name=""):
    if name is None:
        name = ""

    if request.method == 'GET':
        employees = Employed.objects.annotate(full_name=Concat('last_name', 'first_name')).filter(
            full_name__icontains=name)
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
        return JSONResponse(branches_serialized.data)


def branches_by_user_list(request, user_code, branch_name):
    if request.method == 'GET':
        branches_by_user = UserBranch.objects.filter(user__code=user_code, branch__name__istartswith=branch_name,
                                                     state='A')
        branches_by_user_serialized = UserBranchSerializer(branches_by_user, many=True)
        return JSONResponse(branches_by_user_serialized.data)


def order_list(request, date_from, date_to, order_id="", warehouse_id="", branch_id="", travel_id="",
               employed_id="", state="", observation="", provider_name=""):
    if order_id is None:
        order_id = ''
    if warehouse_id is None:
        warehouse_id = ''
    if branch_id is None:
        branch_id = ''
    if travel_id is None:
        travel_id = ''
    if employed_id is None:
        employed_id = ''
    if state is None:
        state = ''
    if observation is None:
        observation = ''
    if provider_name is None:
        provider_name = ''

    if request.method == 'GET':
        response_data = []
        vw_orders_all = ViewOrder.objects.filter(order_id__gte=order_id, warehouse_id__icontains=warehouse_id,
                                                 branch_id__icontains=branch_id,
                                                 travel_id__icontains=travel_id, applicant_id__icontains=employed_id,
                                                 state__icontains=state, observation__icontains=observation,
                                                 provider_name__icontains=provider_name,
                                                 date__range=(date_from, date_to)).order_by('order_id')

        vw_orders_header = vw_orders_all.values('order_id', 'date', 'observation', 'state', 'warehouse_id',
                                                'warehouse_name', 'branch_id', 'branch_name', 'travel_id',
                                                'travel_name', 'applicant_id', 'applicant_name', 'provider_name',
                                                'user_created', 'date_created', 'date_approved').distinct()

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
                          'provider_name': header['provider_name'], 'user_created': header['user_created'],
                          'date_created': header['date_created'], 'date_approved': header['date_approved'],
                          'detail': order_detail_data}

            response_data.append(order_data)

        return JSONResponse(response_data)


def order_detail(request, order_id=""):
    if request.method == 'GET':
        vw_order_all = ViewOrder.objects.filter(order_id__exact=order_id)

        if vw_order_all.__len__() == 0:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        vw_order_header = vw_order_all.values('order_id', 'date', 'observation', 'state', 'warehouse_id',
                                              'warehouse_name', 'branch_id', 'branch_name', 'travel_id',
                                              'travel_name', 'applicant_id', 'applicant_name', 'provider_name',
                                              'user_created', 'date_created', 'date_approved').distinct()[0]

        vw_orders_detail = vw_order_all.filter(order_id=order_id)

        # Order detail to map
        order_detail_data = []
        for detail in vw_orders_detail:
            order_detail_data.append(
                {'sequence': detail.detail_sequence, 'quantity': detail.detail_quantity,
                 'detail': detail.detail_detail})

        # Order header to map
        order_data = {'order_id': vw_order_header['order_id'],
                      'date': vw_order_header['date'],
                      'observation': vw_order_header['observation'],
                      'state': vw_order_header['state'],
                      'warehouse_id': vw_order_header['warehouse_id'],
                      'warehouse_name': vw_order_header['warehouse_name'],
                      'travel_id': vw_order_header['travel_id'],
                      'travel_name': vw_order_header['travel_name'],
                      'branch_id': vw_order_header['branch_id'],
                      'branch_name': vw_order_header['branch_name'],
                      'applicant_id': vw_order_header['applicant_id'],
                      'applicant_name': vw_order_header['applicant_name'],
                      'provider_name': vw_order_header['provider_name'],
                      'user_created': vw_order_header['user_created'],
                      'date_created': vw_order_header['date_created'],
                      'date_approved': vw_order_header['date_approved'],
                      'detail': order_detail_data}

        return JSONResponse(order_data)


@csrf_exempt
def order_create(request):
    # Getting data
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = json.loads(body['order_data'])

    # Getting the new sequence
    new_sequence = Order.objects.order_by("-id")[0].id
    new_sequence += 1

    # Creating the object to save
    order = Order(id=new_sequence, date=content['date'], state='P', observation=content['observation'],
                  warehouse_id=content['warehouse']['code'], branch_id=content['branch']['code'],
                  travel_id=content['travel']['code'], applicant_id=content['applicant']['id'],
                  user_created=content['userCreated'], date_created=content['dateCreated'])

    order.save()

    detail_sequence = 0
    for d in content['detail']:
        detail_sequence += 1
        detail = OrderDetail(order_id=new_sequence, sequence=detail_sequence, quantity=d['quantity'],
                             detail=d['detail'])
        detail.save()

    return JSONResponse({'id': new_sequence}, status=status.HTTP_200_OK)


@csrf_exempt
def order_update(request):
    # Getting data
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = json.loads(body['order_data'])

    print(content)

    date_approved = None
    if content['dateApproved'] != '':
        date_approved = content['dateApproved']

    order_request = Order(id=content['id'], date=content['date'], state=content['state'],
                          observation=content['observation'],
                          warehouse_id=content['warehouse']['code'], branch_id=content['branch']['code'],
                          travel_id=content['travel']['code'], applicant_id=content['applicant']['id'],
                          user_created=content['userCreated'], date_created=content['dateCreated'],
                          date_approved=date_approved)

    # Updating the order
    order_request.save()

    # Deleting the detail in the database
    OrderDetail.objects.filter(order_id__exact=content['id']).delete()

    # Creating the new detail
    detail_sequence = 0
    for d in content['detail']:
        detail_sequence += 1
        detail = OrderDetail(order_id=content['id'], sequence=detail_sequence, quantity=d['quantity'],
                             detail=d['detail'])
        detail.save()

    return JSONResponse(data={}, status=status.HTTP_200_OK)
