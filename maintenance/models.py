from django.db import models


class User(models.Model):
    code = models.CharField(primary_key=True, max_length=10, name='CODIGO', db_column='CODIGO')
    user = models.CharField(max_length=10, name='USUARIO', db_column='USUARIO')
    password = models.CharField(max_length=20, name='CLAVE', db_column='CLAVE')
    name = models.CharField(max_length=40, name='NOMBRE', db_column='NOMBRE')

    class Meta:
        db_table = 'USUARIOS'
