from django.urls import path

from . import views

app_name = 'maintenance'

urlpatterns = [
    path('login/<user>/<password>', views.login, name='login'),
    path('accessByRole/<role_code>', views.accessByRol, name='role_code')
]