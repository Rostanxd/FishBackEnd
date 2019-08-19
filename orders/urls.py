from django.urls import path, re_path

from . import views

app_name = 'orders'

urlpatterns = [
    path('warehouses/<path:name>/', views.warehouse_list, name='warehouse_list'),
    path('travels/<path:name>/', views.travel_list, name='travel_list'),
    path('branches/<path:name>/', views.branch_list, name='branch_list'),
    path('branches_by_user/<user_code>/<path:branch_name>/', views.branches_by_user_list, name='branches_by_user_list'),
    path('employees/<path:name>/', views.employees_list, name='employed_list'),
    re_path(
        r'^list/(?P<date_from>[\w\-]+)/'
        r'(?P<date_to>[\w\-]+)/'
        r'(?:(?P<warehouse_id>[\w\-]+))?/'
        r'(?:(?P<branch_id>[\w\-]+))?/'
        r'(?:(?P<travel_id>[\w\-]+))?/'
        r'(?:(?P<employed_id>[\w\-]+))?/'
        r'(?:(?P<state>[\w\-]+))?/'
        r'(?:(?P<observation>[\w\-]+))?/'
        r'(?:(?P<provider_name>[\w\-]+))?/$',
        views.order_list, name='order_list'),
    path('detail/<order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
]
