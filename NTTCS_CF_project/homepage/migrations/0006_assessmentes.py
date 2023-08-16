# Generated by Django 4.2.2 on 2023-08-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_iniciativas_tiposiniciativas'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentEs',
            fields=[
                ('dominio', models.TextField(blank=True, db_column='Dominio', null=True)),
                ('seleccionado_y_n_field', models.CharField(blank=True, db_column='Seleccionado? (Y/N)', max_length=255, null=True)),
                ('control', models.CharField(blank=True, db_column='Control', max_length=255, null=True)),
                ('id', models.CharField(db_column='ID', max_length=255, primary_key=True, serialize=False)),
                ('descripción_de_control', models.TextField(blank=True, db_column='Descripción de Control', null=True)),
                ('métodos_para_cumplir_con_el_control', models.TextField(blank=True, db_column='Métodos para cumplir con el control', null=True)),
                ('referencias_de_solicitud_de_pruebas', models.TextField(blank=True, db_column='Referencias de solicitud de pruebas', null=True)),
                ('pregunta_de_control', models.TextField(blank=True, db_column='Pregunta de control', null=True)),
                ('campo9', models.TextField(blank=True, db_column='Campo9', null=True)),
                ('campo10', models.TextField(blank=True, db_column='Campo10', null=True)),
                ('campo11', models.TextField(blank=True, db_column='Campo11', null=True)),
                ('campo12', models.TextField(blank=True, db_column='Campo12', null=True)),
                ('campo13', models.TextField(blank=True, db_column='Campo13', null=True)),
                ('campo14', models.TextField(blank=True, db_column='Campo14', null=True)),
                ('evaluación_pregunta_evidencias_comentarios', models.TextField(blank=True, db_column='Evaluación Pregunta/Evidencias Comentarios', null=True)),
                ('resultado_evaluado', models.TextField(blank=True, db_column='Resultado evaluado', null=True)),
                ('owner_de_control', models.TextField(blank=True, db_column='Owner de Control', null=True)),
                ('campo18', models.TextField(blank=True, db_column='Campo18', null=True)),
                ('comentario_control_corporativo_común', models.TextField(blank=True, db_column='Comentario control corporativo común', null=True)),
                ('comentarios_de_evaluación_del_control', models.TextField(blank=True, db_column='Comentarios de evaluación del control', null=True)),
                ('evidencia_solicitada', models.TextField(blank=True, db_column='Evidencia Solicitada', null=True)),
            ],
            options={
                'db_table': 'assessment_es',
                'managed': False,
            },
        ),
    ]