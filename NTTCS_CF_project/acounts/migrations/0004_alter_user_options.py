# Generated by Django 4.2.2 on 2023-07-14 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('puede_exportar', 'Puede exportar assessment'), ('puede_crear_informes', 'Puede crear el informe de algun assesment'), ('puede_Mantener_tablas', 'Puede entrar al mantenimeinto de las tablas'), ('puede_crear_assesment', 'Puede crear assessments'), ('puede_ver_assesment', 'Puede ver los assessments'))},
        ),
    ]
