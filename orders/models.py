from django.db import models

from maintenance.models import User


class Employed(models.Model):
    id = models.CharField(max_length=10, primary_key=True, name='id', db_column='EMPL_CO')
    first_name = models.CharField(max_length=50, name='first_name', db_column='EMPL_NO')
    last_name = models.CharField(max_length=50, name='last_name', db_column='EMPL_AP')

    class Meta:
        db_table = 'TBNOM_EMPLEADO'


class Warehouse(models.Model):
    code = models.CharField(primary_key=True, max_length=10, name='code', db_column='CODIGO')
    data_id = models.CharField(max_length=1, name='data_id', db_column='DATA')
    enterprise_id = models.IntegerField(name='enterprise_id', db_column='EMPRESA')
    name = models.CharField(max_length=200, name='name', db_column='NOMBRE')

    class Meta:
        unique_together = (('code', 'data_id', 'enterprise_id'),)
        db_table = 'ARINDEX'


class Branch(models.Model):
    code = models.CharField(primary_key=True, max_length=5, name='code', db_column='CODIGO')
    name = models.CharField(max_length=100, name='name', db_column='NOMBRE')

    class Meta:
        db_table = 'SUCURSAL'


class UserBranch(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, name='user', db_column='USR_CODIGO')
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, max_length=5, name='branch', db_column='SUC_CODIGO')
    state = models.CharField(max_length=1, name='state', db_column='ESTADO')

    class Meta:
        unique_together = (('user', 'branch'),)
        db_table = 'USUARIOS_SUCURSALES'


class Order(models.Model):
    id = models.IntegerField(primary_key=True, name='id', db_column='PED_ID')
    date = models.DateTimeField(name='date', db_column='PED_FECHA')
    state = models.CharField(max_length=5, name='state', db_column='PED_ST')
    observation = models.CharField(max_length=1000, name='observation', db_column='PED_OBS')
    warehouse = models.OneToOneField(Warehouse, name='warehouse', db_column='PED_BOD', on_delete=models.CASCADE)
    applicant = models.OneToOneField(Employed, name='applicant', db_column='PED_SOL', on_delete=models.CASCADE)

    class Meta:
        db_table = 'TBCPED'


class OrderDetail(models.Model):
    order = models.OneToOneField(Order, primary_key=True, on_delete=models.CASCADE, name='order', db_column='PED_ID')
    sequence = models.IntegerField(name='sequence', db_column='PED_SEC')
    quantity = models.IntegerField(name='quantity', db_column='PED_CANT')
    detail = models.CharField(max_length=1000, name='detail', db_column='PED_DETALLE')

    class Meta:
        unique_together = (('order', 'sequence'),)
        db_table = 'TBDPED'


class ViewOrder(models.Model):
    order_id = models.IntegerField(name='order_id', db_column='PED_ID', primary_key=True)
    date = models.DateTimeField(name='date', db_column='PED_FECHA')
    state = models.CharField(name='state', db_column='PED_ST', max_length=5)
    observation = models.CharField(max_length=1000, name='observation', db_column='PED_OBS')
    warehouse_id = models.CharField(name='warehouse_id', db_column='PED_BOD', max_length=10)
    warehouse_name = models.CharField(name='warehouse_name', db_column='NOM_BODEGA', max_length=200)
    travel_id = models.CharField(name='travel_id', db_column='PED_VIAJE', max_length=10)
    travel_name = models.CharField(name='travel_name', db_column='NOM_VIAJE', max_length=200)
    branch_id = models.CharField(name='branch_id', db_column='PED_SUC', max_length=5)
    branch_name = models.CharField(name='branch_name', db_column='nom_centrocosto', max_length=100)
    employed_id = models.CharField(name='applicant_id', db_column='PED_SOL', max_length=10)
    employed_name = models.CharField(name='applicant_name', db_column='NOM_SOLICITADO', max_length=101)
    provider_name = models.CharField(name='provider_name', db_column='nom_proveedor', max_length=500)
    detail_sequence = models.IntegerField(name='detail_sequence', db_column='PED_SEC')
    detail_quantity = models.IntegerField(name='detail_quantity', db_column='PED_CANT')
    detail_detail = models.CharField(max_length=1000, name='detail_detail', db_column='PED_DETALLE')

    class Meta:
        managed = False
        db_table = 'VW_PEDIDOS'
