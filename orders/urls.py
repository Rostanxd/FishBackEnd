from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('travels/', views.travel_list, name='travel_list'),
    path('branches/', views.branch_list, name='branch_list'),
    path('branches_by_user/<user_code>/', views.branches_by_user_list, name='branches_by_user_list'),
    path('employees/', views.employees_list, name='employed_list'),
    path('list/', views.order_list, name='order_list'),
    path('detail/<order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('update/', views.order_update, name='order_update'),
]
