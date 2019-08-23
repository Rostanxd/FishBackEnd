from django.http import HttpResponse
from rest_framework import status
import datetime

from maintenance.models import User, AccessByRol, UserDeviceAccess
from maintenance.serializers import UserSerializer, AccessByRolSerializer
from orders.views import JSONResponse


def login(request, user, password, device_id):
    try:
        users = User.objects.filter(user=user.upper(), password=password.upper())
        #   Getting the user from the list
        user = users[0]

        #   Saving the register of the authentication in the device
        user_device_access = UserDeviceAccess(date_ini=datetime.datetime.now(), user=user, device_id=device_id)
        user_device_access.save()
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serialized = UserSerializer(user)
        return JSONResponse(user_serialized.data)


def log_out(request, user_code, device_id):
    try:
        user_auth_list = UserDeviceAccess.objects.filter(user__code__icontains=user_code,
                                                         device_id__icontains=device_id, date_end__isnull=True)
        user_auth = user_auth_list[0]
        user_auth.date_end = datetime.datetime.now()
        user_auth.save()
    except IndexError:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return JSONResponse({"response": True}, status=status.HTTP_200_OK)


def access_by_role(request, role_code):
    try:
        access = AccessByRol.objects.filter(role__code=role_code)
    except AccessByRol.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        access_serialized = AccessByRolSerializer(access, many=True)
        return JSONResponse(access_serialized.data)


def user_authenticated(request, device_id):
    user_auth = UserDeviceAccess.objects.filter(device_id__icontains=device_id,
                                                date_end__isnull=True)
    try:
        user = user_auth[0].user
        data = UserSerializer(user).data
    except IndexError:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return JSONResponse(data, status=status.HTTP_200_OK)
