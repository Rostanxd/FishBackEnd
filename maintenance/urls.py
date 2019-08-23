from django.urls import path

from . import views

app_name = 'maintenance'

urlpatterns = [
    path('login/<user>/<password>/<device_id>', views.login, name='login'),
    path('logOut/<user_code>/<device_id>', views.logOut, name='logOut'),
    path('accessByRole/<role_code>', views.accessByRol, name='role_code'),
    path('userAuthenticated/<user_code>/<device_id>', views.userAuthenticated, name='userAuthenticated'),
]
