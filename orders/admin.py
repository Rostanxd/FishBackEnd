from django.contrib import admin
from orders.models import Order, OrderDetail, Warehouse, Employed

admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Warehouse)
admin.site.register(Employed)
