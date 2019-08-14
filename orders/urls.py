from django.urls import path, re_path

from . import views

app_name = 'orders'

urlpatterns = [
    path('employees', views.employees_list, name='employed_list'),
    path('employed/<pk>/', views.employed_detail, name='employed_detail'),
    path('warehouse/<id>/<data_id>/<enterprise_id>/', views.warehouse_detail, name='warehouse_detail'),
    path('warehouses/<path:name>/', views.warehouse_list, name='warehouse_list'),
    path('branches/<path:name>/', views.branch_list, name='branch_list'),
    path('branches_by_user/<user_code>/<path:branch_name>/', views.branches_by_user_list, name='branches_by_user_list'),
    re_path(
        r'^list/(?P<date_from>[\w\-]+)/'
        r'(?P<date_to>[\w\-]+)/'
        r'(?:(?P<warehouse_id>[\w\-]+))?/'
        r'(?:(?P<branch_id>[\w\-]+))?/'
        r'(?:(?P<state>[\w\-]+))?/'
        r'(?:(?P<observation>[\w\-]+))?/$',
        views.order_list, name='order_list'),
]
