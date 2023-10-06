from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# Create your models here.

class User(AbstractUser):

    rol = models.CharField(max_length=100, db_column='rol')
    objects = models.Manager()
    REQUIRED_FIELDS = ['rol']
    objects = UserManager()

    class Meta:
        permissions = (
            ('puede_exportar', 'Puede exportar assessment'),
            ('puede_crear_informes', 'Puede crear el informe de algun assesment'),
            ('puede_Mantener_tablas', 'Puede entrar al mantenimeinto de las tablas'),
            ('puede_crear_assesment', 'Puede crear assessments'),
            ('puede_ver_assesment', 'Puede ver los assessments')
        )

