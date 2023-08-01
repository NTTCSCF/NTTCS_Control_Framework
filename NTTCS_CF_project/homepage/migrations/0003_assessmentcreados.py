# Generated by Django 4.2.2 on 2023-08-01 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_mapeomarcos'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentCreados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_id', models.CharField(max_length=100)),
                ('control_name', models.TextField()),
                ('descripcion', models.TextField()),
                ('pregunta', models.TextField()),
                ('criteriovaloracion', models.TextField(blank=True, db_column='criterioValoracion', null=True)),
                ('respuesta', models.TextField(blank=True, null=True)),
                ('valoracion', models.TextField(blank=True, null=True)),
                ('evidencia', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'assessment_creados',
                'managed': False,
            },
        ),
    ]
