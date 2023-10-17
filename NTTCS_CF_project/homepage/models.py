# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models

class AsociacionMarcos(models.Model):
    marco_id = models.CharField(primary_key=True, max_length=255)
    nombre_tabla = models.CharField(max_length=255, blank=True, null=True)
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'asociacion_marcos'


class Assessment(models.Model):
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    selected = models.CharField(db_column='Selected', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    control = models.CharField(db_column='Control', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=255, primary_key=True)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control Description', max_length=255, blank=True,
                                           null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    methods_to_comply_with_control = models.CharField(db_column='Methods To Comply With Control', max_length=255,
                                                      blank=True,
                                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    evidence_request_references = models.CharField(db_column='Evidence Request References', max_length=255, blank=True,
                                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_question = models.CharField(db_column='Control Question', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campo9 = models.CharField(db_column='Campo9', max_length=255, blank=True, null=True)  # Field name made lowercase.
    campo10 = models.TextField(db_column='Campo10', blank=True, null=True)  # Field name made lowercase.
    campo11 = models.TextField(db_column='Campo11', blank=True, null=True)  # Field name made lowercase.
    campo12 = models.TextField(db_column='Campo12', blank=True, null=True)  # Field name made lowercase.
    campo13 = models.TextField(db_column='Campo13', blank=True, null=True)  # Field name made lowercase.
    campo14 = models.TextField(db_column='Campo14', blank=True, null=True)  # Field name made lowercase.
    assessment_question_evidences_comments = models.CharField(db_column='Assessment Question/Evidences Comments',
                                                              max_length=255, blank=True,
                                                              null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assesed_result = models.CharField(db_column='Assesed result', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_assessment_comments2 = models.CharField(db_column='Control Assessment Comments2', max_length=255,
                                                    blank=True,
                                                    null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'assessment'


class AssessmentEs(models.Model):
    dominio = models.TextField(db_column='Dominio', blank=True, null=True)  # Field name made lowercase.
    seleccionado_y_n_field = models.CharField(db_column='Seleccionado? (Y/N)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    control = models.CharField(db_column='Control', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    control_description = models.TextField(db_column='Descripción de Control', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    métodos_para_cumplir_con_el_control = models.TextField(db_column='Métodos para cumplir con el control', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    referencias_de_solicitud_de_pruebas = models.TextField(db_column='Referencias de solicitud de pruebas', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_question = models.TextField(db_column='Pregunta de control', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campo9 = models.TextField(db_column='Campo9', blank=True, null=True)  # Field name made lowercase.
    campo10 = models.TextField(db_column='Campo10', blank=True, null=True)  # Field name made lowercase.
    campo11 = models.TextField(db_column='Campo11', blank=True, null=True)  # Field name made lowercase.
    campo12 = models.TextField(db_column='Campo12', blank=True, null=True)  # Field name made lowercase.
    campo13 = models.TextField(db_column='Campo13', blank=True, null=True)  # Field name made lowercase.
    campo14 = models.TextField(db_column='Campo14', blank=True, null=True)  # Field name made lowercase.
    evaluación_pregunta_evidencias_comentarios = models.TextField(db_column='Evaluación Pregunta/Evidencias Comentarios', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    resultado_evaluado = models.TextField(db_column='Resultado evaluado', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    owner_de_control = models.TextField(db_column='Owner de Control', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campo18 = models.TextField(db_column='Campo18', blank=True, null=True)  # Field name made lowercase.
    comentario_control_corporativo_común = models.TextField(db_column='Comentario control corporativo común', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comentarios_de_evaluación_del_control = models.TextField(db_column='Comentarios de evaluación del control', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    evidencia_solicitada = models.TextField(db_column='Evidencia Solicitada', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'assessment_es'

class Assessmentguardados(models.Model):
    id_assessment = models.CharField(db_column='ID_assessment', primary_key=True, max_length=100)  # Field name made lowercase.
    marcos = models.TextField(blank=True, null=True)
    archivado = models.IntegerField(blank=True, null=True)
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    idioma = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    fecha_ultima_modificacion = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    plan_proyecto_mejora = models.ForeignKey('PlanProyectoMejora', models.DO_NOTHING, db_column='plan_proyecto_mejora', blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'assessmentguardados'

class AssessmentCreados(models.Model):
    assessment = models.ForeignKey('Assessmentguardados', models.DO_NOTHING, db_column='assessment')
    control_id = models.CharField(max_length=100)
    control_name = models.TextField()
    descripcion = models.TextField()
    pregunta = models.TextField()
    criteriovaloracion = models.TextField(db_column='criterioValoracion', blank=True, null=True)  # Field name made lowercase.
    respuesta = models.TextField(blank=True, null=True)
    valoracion = models.TextField(blank=True, null=True)
    valoracionobjetivo = models.TextField(db_column='valoracionObjetivo', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'assessment_creados'

class AsociacionEvidenciasGenericas(models.Model):
    evidencia = models.ForeignKey('Evidencerequestcatalog', models.DO_NOTHING, blank=True, null=True)
    assessment = models.ForeignKey('AssessmentCreados', models.DO_NOTHING, db_column='assessment')
    iniciativa = models.ForeignKey('Iniciativas', models.DO_NOTHING, db_column='iniciativa', blank=True, null=True)
    evidencia_id_es = models.ForeignKey('EvidencerequestcatalogEs', models.DO_NOTHING, db_column='evidencia_id_es', blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_evidencias_genericas'

class AsociacionEvidenciasCreadas(models.Model):
    id_evidencia = models.ForeignKey('Evidencias', models.DO_NOTHING, db_column='Id_evidencia')  # Field name made lowercase.
    id_assessment = models.ForeignKey('AssessmentCreados', models.DO_NOTHING, db_column='id_assessment')
    iniciativa = models.ForeignKey('Iniciativas', models.DO_NOTHING, db_column='iniciativa', blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_evidencias_creadas'

class TiposIniciativas(models.Model):
    tipo = models.TextField()
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'tipos_iniciativas'

class Iniciativas(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')  # Field name made lowercase.
    tipo = models.ForeignKey('TiposIniciativas', models.DO_NOTHING, db_column='tipo')
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iniciativas'

class Proyecto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=100)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='cliente', blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'proyecto'

class AsociacionUsuariosProyecto(models.Model):
    usuario = models.ForeignKey('acounts.User', models.DO_NOTHING, db_column='usuario')
    proyecto = models.ForeignKey('Proyecto', models.DO_NOTHING, db_column='proyecto')
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_usuarios_proyecto'

class AsociacionProyectoAssessment(models.Model):
    assessment = models.ForeignKey('Assessmentguardados', models.DO_NOTHING, db_column='assessment')
    proyecto = models.ForeignKey('Proyecto', models.DO_NOTHING, db_column='proyecto')
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_proyecto_assessment'

class PlanProyectoMejora(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'plan_proyecto_mejora'

class AsociacionPlanProyectosProyectos(models.Model):
    proyecto_mejora = models.ForeignKey('ProyectosMejora', models.DO_NOTHING, db_column='proyecto_mejora', blank=True, null=True)
    plan_proyecto = models.ForeignKey('PlanProyectoMejora', models.DO_NOTHING, db_column='plan_proyecto', blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_plan_proyectos_proyectos'

class ProyectosMejora(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    riesgos = models.TextField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    duracion = models.FloatField(blank=True, null=True)
    capex = models.FloatField(blank=True, null=True)
    beneficio = models.FloatField(blank=True, null=True)
    opex = models.FloatField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'proyectos_mejora'

class AsociacionProyectoMejoraIniciativa(models.Model):
    proyecto = models.ForeignKey('ProyectosMejora', models.DO_NOTHING, db_column='proyecto')
    iniciativa = models.ForeignKey('Iniciativas', models.DO_NOTHING, db_column='iniciativa')
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_proyecto_mejora_iniciativa'

class DependenciaProyecto(models.Model):
    proyecto = models.ForeignKey('ProyectosMejora', models.DO_NOTHING, db_column='proyecto')
    proyecto_asociado = models.ForeignKey('ProyectosMejora', models.DO_NOTHING, db_column='proyecto_asociado', related_name='dependenciaproyecto_proyecto_asociado_set')
    porcentaje = models.IntegerField()
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'dependencia_proyecto'

class Entrevistas(models.Model):
    titulo = models.CharField(db_column='Titulo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateTimeField(blank=True, null=True)
    grupocontroles = models.TextField(db_column='grupoControles', blank=True, null=True)  # Field name made lowercase.
    area = models.TextField(blank=True, null=True)
    creador = models.ForeignKey('acounts.User', models.DO_NOTHING, db_column='creador', blank=True, null=True)
    duracionestimada = models.TimeField(db_column='duracionEstimada', blank=True, null=True)  # Field name made lowercase.
    duracionreal = models.TimeField(db_column='duracionReal', blank=True, null=True)  # Field name made lowercase.
    assesment = models.ForeignKey('Assessmentguardados', models.DO_NOTHING, db_column='assesment')
    editor = models.ForeignKey('acounts.User', models.DO_NOTHING, db_column='editor', related_name='entrevistas_editor_set', blank=True, null=True)
    asistentes = models.TextField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'entrevistas'

class AsociacionEntrevistasUsuarios(models.Model):
    entrevista = models.ForeignKey('Entrevistas', models.DO_NOTHING, db_column='entrevista')
    usuario = models.ForeignKey('acounts.User', models.DO_NOTHING, db_column='usuario')
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_entrevistas_usuarios'

class Cliente(models.Model):
    codigo = models.CharField(primary_key=True, max_length=100)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="images/", null=True, blank=True)
    alcance = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'cliente'

class AuthGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=150)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_group'


class MapeoMarcos(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', primary_key=True, max_length=255)  # Field name made lowercase.
    ciscscv8 = models.IntegerField(db_column='CISCSCv8', blank=True, null=True)  # Field name made lowercase.
    cobit2019 = models.IntegerField(db_column='COBIT2019', blank=True, null=True)  # Field name made lowercase.
    cosov2017 = models.IntegerField(db_column='COSOv2017', blank=True, null=True)  # Field name made lowercase.
    csaccmv4 = models.IntegerField(db_column='CSACCMv4', blank=True, null=True)  # Field name made lowercase.
    csaiotscfv2 = models.IntegerField(db_column='CSAIoTSCFv2', blank=True, null=True)  # Field name made lowercase.
    enisav2 = models.IntegerField(db_column='ENISAv2', blank=True, null=True)  # Field name made lowercase.
    iec6244342 = models.IntegerField(db_column='IEC6244342', blank=True, null=True)  # Field name made lowercase.
    iso22301v2019 = models.IntegerField(db_column='ISO22301v2019', blank=True, null=True)  # Field name made lowercase.
    iso27001v2013 = models.IntegerField(db_column='ISO27001v2013', blank=True, null=True)  # Field name made lowercase.
    iso27001v2022 = models.IntegerField(db_column='ISO27001v2022', blank=True, null=True)  # Field name made lowercase.
    iso27002v2013 = models.IntegerField(db_column='ISO27002v2013', blank=True, null=True)  # Field name made lowercase.
    iso27002v2022 = models.IntegerField(db_column='ISO27002v2022', blank=True, null=True)  # Field name made lowercase.
    iso27017v2015 = models.IntegerField(db_column='ISO27017v2015', blank=True, null=True)  # Field name made lowercase.
    iso27018v2014 = models.IntegerField(db_column='ISO27018v2014', blank=True, null=True)  # Field name made lowercase.
    iso27701v2019 = models.IntegerField(db_column='ISO27701v2019', blank=True, null=True)  # Field name made lowercase.
    iso29100v2011 = models.IntegerField(db_column='ISO29100v2011', blank=True, null=True)  # Field name made lowercase.
    iso31000v2009 = models.IntegerField(db_column='ISO31000v2009', blank=True, null=True)  # Field name made lowercase.
    iso31010v2009 = models.IntegerField(db_column='ISO31010v2009', blank=True, null=True)  # Field name made lowercase.
    nistarmfai1001v1 = models.IntegerField(db_column='NISTARMFAI1001v1', blank=True, null=True)  # Field name made lowercase.
    nistprivacyframeworkv1 = models.IntegerField(db_column='NISTPrivacyFrameworkv1', blank=True, null=True)  # Field name made lowercase.
    nistssdf = models.IntegerField(db_column='NISTSSDF', blank=True, null=True)  # Field name made lowercase.
    nist80037rev2 = models.IntegerField(db_column='NIST80037rev2', blank=True, null=True)  # Field name made lowercase.
    nist80039 = models.IntegerField(db_column='NIST80039', blank=True, null=True)  # Field name made lowercase.
    nist80053rev4 = models.IntegerField(db_column='NIST80053rev4', blank=True, null=True)  # Field name made lowercase.
    nist80053rev4low = models.IntegerField(blank=True, null=True)
    nist80053rev4moderate = models.IntegerField(blank=True, null=True)
    nist80053rev4high = models.IntegerField(db_column='NIST80053rev4high', blank=True, null=True)  # Field name made lowercase.
    nist80053rev5 = models.IntegerField(db_column='NIST80053rev5', blank=True, null=True)  # Field name made lowercase.
    nist80053rev5privacy = models.IntegerField(blank=True, null=True)
    nist80053rev5low = models.IntegerField(blank=True, null=True)
    nist80053rev5moderate = models.IntegerField(blank=True, null=True)
    nist80053rev5high = models.IntegerField(blank=True, null=True)
    nist80053rev5noc = models.IntegerField(blank=True, null=True)
    nist80063bpartialmapping = models.IntegerField(blank=True, null=True)
    nist80082rev2lowimpacticsoverlay = models.IntegerField(db_column='NIST80082rev2LowImpactICSOverlay', blank=True, null=True)  # Field name made lowercase.
    nist80082rev2moderateimpacticsoverlay = models.IntegerField(db_column='NIST80082rev2ModerateImpactICSOverlay', blank=True, null=True)  # Field name made lowercase.
    nist80082rev2highimpacticsoverlay = models.IntegerField(db_column='NIST80082rev2HighImpactICSOverlay', blank=True, null=True)  # Field name made lowercase.
    nist800160 = models.IntegerField(db_column='NIST800160', blank=True, null=True)  # Field name made lowercase.
    nist800161rev1 = models.IntegerField(db_column='NIST800161rev1', blank=True, null=True)  # Field name made lowercase.
    nist800161rev1cscrmbaseline = models.IntegerField(db_column='NIST800161rev1CSCRMBaseline', blank=True, null=True)  # Field name made lowercase.
    nist800161rev1flowdown = models.IntegerField(db_column='NIST800161rev1FlowDown', blank=True, null=True)  # Field name made lowercase.
    nist800161rev1level1 = models.IntegerField(db_column='NIST800161rev1Level1', blank=True, null=True)  # Field name made lowercase.
    nist800161rev1level2 = models.IntegerField(db_column='NIST800161rev1Level2', blank=True, null=True)  # Field name made lowercase.
    nist800161rev1level3 = models.IntegerField(db_column='NIST800161rev1Level3', blank=True, null=True)  # Field name made lowercase.
    nist800171rev2 = models.IntegerField(db_column='NIST800171rev2', blank=True, null=True)  # Field name made lowercase.
    nist800171a = models.IntegerField(db_column='NIST800171A', blank=True, null=True)  # Field name made lowercase.
    nist800172 = models.IntegerField(db_column='NIST800172', blank=True, null=True)  # Field name made lowercase.
    nist800218v1_1 = models.IntegerField(db_column='NIST800218v1_1', blank=True, null=True)  # Field name made lowercase.
    nistcsfv1_1 = models.IntegerField(db_column='NISTCSFv1_1', blank=True, null=True)  # Field name made lowercase.
    owasptop10v2021 = models.IntegerField(db_column='OWASPTop10v2021', blank=True, null=True)  # Field name made lowercase.
    pcidssv3_2 = models.IntegerField(db_column='PCIDSSv3_2', blank=True, null=True)  # Field name made lowercase.
    pcidssv4_0 = models.IntegerField(db_column='PCIDSSv4_0', blank=True, null=True)  # Field name made lowercase.
    usc2m2v2_1 = models.IntegerField(db_column='USC2M2v2_1', blank=True, null=True)  # Field name made lowercase.
    uscertrmmv1_2 = models.IntegerField(db_column='USCERTRMMv1_2', blank=True, null=True)  # Field name made lowercase.
    uscmmc2_0level1 = models.IntegerField(db_column='USCMMC2_0Level1', blank=True, null=True)  # Field name made lowercase.
    uscmmc2_0level2 = models.IntegerField(db_column='USCMMC2_0Level2', blank=True, null=True)  # Field name made lowercase.
    uscmmc2_0level3 = models.IntegerField(db_column='USCMMC2_0Level3', blank=True, null=True)  # Field name made lowercase.
    ushipaa = models.IntegerField(db_column='USHIPAA', blank=True, null=True)  # Field name made lowercase.
    hipaahicpsmallpractice = models.IntegerField(db_column='HIPAAHICPSmallPractice', blank=True, null=True)  # Field name made lowercase.
    hipaahicpmediumpractice = models.IntegerField(db_column='HIPAAHICPMediumPractice', blank=True, null=True)  # Field name made lowercase.
    hipaahicplargepractice = models.IntegerField(db_column='HIPAAHICPLargePractice', blank=True, null=True)  # Field name made lowercase.
    ussox = models.IntegerField(db_column='USSOX', blank=True, null=True)  # Field name made lowercase.
    emeaeudora = models.IntegerField(db_column='EMEAEUDORA', blank=True, null=True)  # Field name made lowercase.
    emeaeueprivacydraft = models.IntegerField(db_column='EMEAEUePrivacydraft', blank=True, null=True)  # Field name made lowercase.
    emeaeugdpr = models.IntegerField(db_column='EMEAEUGDPR', blank=True, null=True)  # Field name made lowercase.
    emeaeupsd2 = models.IntegerField(db_column='EMEAEUPSD2', blank=True, null=True)  # Field name made lowercase.
    emeaspain = models.IntegerField(db_column='EMEASpain', blank=True, null=True)  # Field name made lowercase.
    emeaspainccnstic825 = models.IntegerField(db_column='EMEASpainCCNSTIC825', blank=True, null=True)  # Field name made lowercase.
    scfbbusinessmergersacquisitions = models.IntegerField(db_column='SCFBBusinessMergersAcquisitions', blank=True, null=True)  # Field name made lowercase.
    scficyberinsurance = models.IntegerField(db_column='SCFICyberInsurance', blank=True, null=True)  # Field name made lowercase.
    scfeembeddedtechnology = models.IntegerField(db_column='SCFEEmbeddedTechnology', blank=True, null=True)  # Field name made lowercase.
    scfrransomwareprotection = models.IntegerField(db_column='SCFRRansomwareProtection', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'mapeo_marcos'
class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    ntt_id = models.BigAutoField(db_column='NTT_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'django_session'


class Domains(models.Model):
    identifier = models.CharField(db_column='Identifier', primary_key=True,
                                  max_length=255)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    security_privacy_by_design_s_p_principles = models.CharField(
        db_column='Security & Privacy by Design (S|P) Principles', max_length=255, blank=True,
        null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    principle_intent = models.TextField(db_column='Principle Intent', blank=True,
                                        null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'domains'


class Evidencerequestcatalog(models.Model):
    evidence_request_references = models.CharField(db_column='Evidence Request References', primary_key=True,
                                                   max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_focus = models.CharField(db_column='Area of Focus', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    artifact = models.CharField(db_column='Artifact', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    artifact_description = models.TextField(db_column='Artifact Description', blank=True,
                                            null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_mappings = models.CharField(db_column='Control Mappings', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'evidencerequestcatalog'

class EvidencerequestcatalogEs(models.Model):
    evidence_request_references = models.CharField(db_column='Evidence Request References', primary_key=True, max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_focus = models.CharField(db_column='Area of Focus', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    artifact = models.CharField(db_column='Artifact', max_length=255, blank=True, null=True)  # Field name made lowercase.
    artifact_description = models.TextField(db_column='Artifact Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_mappings = models.CharField(db_column='Control Mappings', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'evidencerequestcatalog_es'


class Evidencias(models.Model):
    evidencia_id = models.CharField(primary_key=True, max_length=100)
    comentario = models.TextField(db_column='Comentario', blank=True, null=True)  # Field name made lowercase.
    links = models.TextField(blank=True, null=True)
    assessment = models.ForeignKey(Assessmentguardados, models.DO_NOTHING, blank=True, null=True)
    control_id = models.CharField(max_length=100, blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'evidencias'


class SeleccionAssessment(models.Model):
    id = models.BigAutoField(primary_key=True)
    seleccion = models.CharField(max_length=255, blank=True, null=True)
    valor = models.CharField(max_length=255, blank=True, null=True)
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'homepage_seleccionassessment'


class MaturirtyTable(models.Model):
    ccmmcod = models.CharField(db_column='CCMMCOD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    sublevels = models.CharField(db_column='SUBLEVELS', primary_key=True, max_length=255)  # Field name made lowercase.
    percentage = models.FloatField(db_column='PERCENTAGE', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'maturirty_table'

class MaturirtyTableEs(models.Model):
    ccmmcod = models.CharField(db_column='CCMMCOD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    sublevels = models.CharField(db_column='SUBLEVELS', primary_key=True, max_length=255)  # Field name made lowercase.
    percentage = models.FloatField(db_column='PERCENTAGE', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'maturirty_table_es'


class NttcsCf20231(models.Model):
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    selected_y_n_field = models.CharField(db_column='Selected? (Y/N)', max_length=255, blank=True,
                                          null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    control = models.CharField(db_column='Control', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control Description', max_length=255, blank=True,
                                           null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relative_control_weighting = models.FloatField(db_column='Relative Control Weighting', blank=True,
                                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    function_grouping = models.CharField(db_column='Function Grouping', max_length=255, blank=True,
                                         null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    scrm1 = models.CharField(db_column='SCRM1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scrm2 = models.CharField(db_column='SCRM2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scrm3 = models.CharField(db_column='SCRM3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assesed_result = models.CharField(db_column='Assesed result', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    numeric_result = models.CharField(db_column='Numeric result', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    weighted_numeric_result = models.FloatField(db_column='Weighted Numeric result', blank=True,
                                                null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assessment_comments = models.CharField(db_column='Assessment Comments', max_length=255, blank=True,
                                           null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relative_result_by_function = models.FloatField(db_column='Relative result by Function', blank=True,
                                                    null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relative_result_by_domain = models.FloatField(db_column='Relative result by Domain', blank=True,
                                                  null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'nttcs cf 2023 1'


class RiskCatalog(models.Model):
    risk_grouping = models.CharField(db_column='Risk Grouping', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    risk_id = models.CharField(db_column='Risk ID', primary_key=True,
                               max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    risk = models.CharField(db_column='Risk', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description_of_possible_risk_due_to_control_deficiency = models.CharField(
        db_column='Description of Possible Risk Due To Control Deficiency', max_length=255, blank=True,
        null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    frequency = models.CharField(db_column='Frequency', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    freqnum = models.FloatField(db_column='FreqNum', blank=True, null=True)  # Field name made lowercase.
    impact = models.CharField(db_column='Impact', max_length=255, blank=True, null=True)  # Field name made lowercase.
    impactnum = models.FloatField(db_column='ImpactNum', blank=True, null=True)  # Field name made lowercase.
    risk_val = models.FloatField(db_column='Risk Val', blank=True,
                                 null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    function = models.CharField(db_column='Function', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'risk catalog'


class ThreatCatalog(models.Model):
    threat_group = models.CharField(db_column='Threat Group', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    threat_id = models.CharField(db_column='Threat ID', primary_key=True,
                                 max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    threat = models.CharField(db_column='Threat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    threat_description = models.TextField(db_column='Threat Description', blank=True,
                                          null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'threat catalog'
