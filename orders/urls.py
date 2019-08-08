from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('employees', views.employees_list, name='employed_list'),
    path('employed/<pk>/', views.employed_detail, name='employed_detail'),
    path('warehouses', views.warehouse_list, name='warehouse_list'),
    path('warehouse/<id>/<data_id>/<enterprise_id>/', views.warehouse_detail, name='warehouse_detail'),
    path('list', views.order_list, name='order_list'),
]
