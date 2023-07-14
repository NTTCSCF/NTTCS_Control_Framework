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


class Assessmentguardados(models.Model):
    id_assessment = models.CharField(db_column='ID_assessment', primary_key=True,
                                     max_length=100)  # Field name made lowercase.
    marcos = models.TextField(blank=True, null=True)
    archivado = models.IntegerField(blank=True, null=True)
    comentario2 = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'assessmentguardados'


class AuthGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=150)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'auth_group'


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
        db_table = 'maturirty table'


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
