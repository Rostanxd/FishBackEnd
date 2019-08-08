from django.db import models


class Employed(models.Model):
    id = models.CharField(max_length=10, primary_key=True, name='EMPL_CO')
    first_name = models.CharField(max_length=50, name='EMPL_NO')
    last_name = models.CharField(max_length=50, name='EMPL_AP')

    class Meta:
        db_table = 'TBNOM_EMPLEADO'


class Warehouse(models.Model):
    code = models.CharField(primary_key=True, max_length=10, name='CODIGO')
    data_id = models.CharField(max_length=1, name='DATA')
    enterprise_id = models.IntegerField(name='EMPRESA')
    name = models.CharField(max_length=200, name='NOMBRE')

    class Meta:
        unique_together = (('CODIGO', 'DATA', 'EMPRESA'),)
        db_table = 'ARINDEX'


class Order(models.Model):
    id = models.IntegerField(primary_key=True, name='PED_ID')
    date = models.DateTimeField(name='PED_FECHA')
    state = models.CharField(max_length=5, name='PED_ST')
    observation = models.CharField(max_length=1000, name='PED_OBS')
    warehouse = models.OneToOneField(Warehouse, name='PED_BOD', db_column='PED_BOD', on_delete=models.CASCADE)
    applicant = models.OneToOneField(Employed, name='PED_SOL', db_column='PED_SOL', on_delete=models.CASCADE)

    class Meta:
        db_table = 'TBCPED'


class OrderDetail(models.Model):
    order = models.OneToOneField(Order, primary_key=True, on_delete=models.CASCADE, name='PED_ID', db_column='PED_ID')
    sequence = models.IntegerField(name='PED_SEC')
    quantity = models.IntegerField(name='PED_CANT')
    detail = models.CharField(max_length=1000, name='PED_DETALLE')

    class Meta:
        unique_together = (('PED_ID', 'PED_SEC'),)
        db_table = 'TBDPED'


class ViewOrder(models.Model):
    order_id = models.IntegerField(name='PED_ID', db_column='PED_ID', primary_key=True)
    date = models.DateTimeField(name='PED_FECHA', db_column='PED_FECHA')
    state = models.CharField(name='PED_ST', db_column='PED_ST', max_length=5)
    warehouse_id = models.CharField(name='PED_BOD', db_column='PED_BOD', max_length=10)
    warehouse_name = models.CharField(name='NOM_BODEGA', db_column='NOM_BODEGA', max_length=200)
    employed_id = models.CharField(name='PED_SOL', db_column='PED_SOL', max_length=10)
    employed_name = models.CharField(name='NOM_SOLICITADO', db_column='NOM_SOLICITADO', max_length=101)
    detail_sequence = models.IntegerField(name='PED_SEC', db_column='PED_SEC')

    class Meta:
        managed = False
        db_table = 'VW_PEDIDOS'
