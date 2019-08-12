from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('employees', views.employees_list, name='employed_list'),
    path('employed/<pk>/', views.employed_detail, name='employed_detail'),
    path('warehouses/<name>/', views.warehouse_list, name='warehouse_list'),
    path('warehouse/<id>/<data_id>/<enterprise_id>/', views.warehouse_detail, name='warehouse_detail'),
    path('branches/<name>/', views.branch_list, name='branch_list'),
    path('branches_by_user/<user_code>/<branch_name>/', views.branches_by_user_list, name='branches_by_user_list'),
    path('list/<date_from>/<date_to>/', views.order_list, name='order_list'),
    path('list/<warehouse_id>/<date_from>/<date_to>/', views.order_list, name='order_list'),
    path('list/<branch_id>/<date_from>/<date_to>/', views.order_list, name='order_list'),
    path('list/<warehouse_id>/<branch_id>/<date_from>/<date_to>/', views.order_list, name='order_list'),
]
