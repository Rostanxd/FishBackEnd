from django.http import HttpResponse
from rest_framework import status

from maintenance.models import User, AccessByRol
from maintenance.serializers import UserSerializer, AccessByRolSerializer
from orders.views import JSONResponse


def login(request, user, password):
    try:
        users = User.objects.filter(user=user.upper(), password=password.upper())
        if users.count() != 0:
            user = users[0]
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serialized = UserSerializer(user)
        return JSONResponse(user_serialized.data)


def accessByRol(request, role_code):
    try:
        access = AccessByRol.objects.filter(role__code=role_code)
    except AccessByRol.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        access_serialized = AccessByRolSerializer(access, many=True)
        return JSONResponse(access_serialized.data)
