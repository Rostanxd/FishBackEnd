from django.db import models


class Program(models.Model):
    code = models.CharField(primary_key=True, max_length=3, name='code', db_column='CODIGO')
    name = models.CharField(max_length=40, name='name', db_column='NOMBRE')

    class Meta:
        db_table = 'PROGRAMAS_APP'


class Role(models.Model):
    code = models.CharField(primary_key=True, max_length=2, name='code', db_column='CODIGO')
    name = models.CharField(max_length=40, name='name', db_column='NOMBRE')

    class Meta:
        db_table = 'ROL_APP'


class User(models.Model):
    code = models.CharField(primary_key=True, max_length=10, name='code', db_column='CODIGO')
    user = models.CharField(max_length=10, name='user', db_column='USUARIO')
    password = models.CharField(max_length=20, name='password', db_column='CLAVE')
    name = models.CharField(max_length=40, name='name', db_column='NOMBRE')
    role = models.OneToOneField(Role, on_delete=models.CASCADE, name='role', db_column='ROL_CODIGO')

    class Meta:
        db_table = 'USUARIOS'


class AccessByRol(models.Model):
    role = models.OneToOneField(Role, primary_key=True, on_delete=models.CASCADE, max_length=2, name='role',
                                db_column='ROL_CODIGO')
    program = models.OneToOneField(Program, on_delete=models.CASCADE, max_length=3, name='program',
                                   db_column='PRG_CODIGO')
    execute = models.CharField(max_length=1, name='execute', db_column='EJECUTAR')
    register = models.CharField(max_length=1, name='register', db_column='REGISTRAR')
    edit = models.CharField(max_length=1, name='edit', db_column='EDITAR')
    delete = models.CharField(max_length=1, name='delete', db_column='ELIMINAR')
    process = models.CharField(max_length=1, name='process', db_column='PROCESAR')

    class Meta:
        unique_together = (('role', 'program'),)
        db_table = 'ROL_APP_ACCESOS'
