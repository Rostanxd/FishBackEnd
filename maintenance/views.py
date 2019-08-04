from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status

from maintenance.models import User
from maintenance.serializers import UserSerializer
from orders.views import JSONResponse


def login(request, user, password):
    try:
        users = User.objects.filter(USUARIO=user, CLAVE=password)
        if users.count() != 0:
            user = users[0]
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serialized = UserSerializer(user)
        return JSONResponse(user_serialized.data)
