from django.urls import path

from . import views

app_name = 'maintenance'

urlpatterns = [
    path('login/<user>/<password>/<device_id>', views.login, name='login'),
    path('logOut/<user_code>/<device_id>', views.log_out, name='logOut'),
    path('accessByRole/<role_code>', views.access_by_role, name='role_code'),
    path('userAuthenticated/<device_id>', views.user_authenticated, name='userAuthenticated'),
]
