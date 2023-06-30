# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AsociacionMarcos(models.Model):
    marco_id = models.CharField(max_length=255, blank=True, primary_key=True)
    nombre_tabla = models.CharField(max_length=255, blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'asociacion_marcos'


class Assessment(models.Model):
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    selected = models.CharField(db_column='Selected', max_length=255, blank=True, null=True)  # Field name made lowercase.
    control = models.CharField(db_column='Control', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control Description', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    methods_to_comply_with_control = models.CharField(db_column='Methods To Comply With Control', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    evidence_request_references = models.CharField(db_column='Evidence Request References', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_question = models.CharField(db_column='Control Question', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    campo9 = models.CharField(db_column='Campo9', max_length=255, blank=True, null=True)  # Field name made lowercase.
    campo10 = models.TextField(db_column='Campo10', blank=True, null=True)  # Field name made lowercase.
    campo11 = models.TextField(db_column='Campo11', blank=True, null=True)  # Field name made lowercase.
    campo12 = models.TextField(db_column='Campo12', blank=True, null=True)  # Field name made lowercase.
    campo13 = models.TextField(db_column='Campo13', blank=True, null=True)  # Field name made lowercase.
    campo14 = models.TextField(db_column='Campo14', blank=True, null=True)  # Field name made lowercase.
    assessment_question_evidences_comments = models.CharField(db_column='Assessment Question/Evidences Comments', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assesed_result = models.CharField(db_column='Assesed result', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_assessment_comments2 = models.CharField(db_column='Control Assessment Comments2', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'assessment'


class Assessmentguardados(models.Model):
    id_assessment = models.CharField(db_column='ID_assessment', primary_key=True, max_length=100)  # Field name made lowercase.
    marcos = models.TextField(blank=True, null=True)
    archivado = models.IntegerField(blank=True, null=True)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'assessmentguardados'


class AuthGroup(models.Model):
    ntt_id = models.AutoField(db_column='NTT_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=150)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    ntt_id = models.BigAutoField(db_column='NTT_ID', primary_key=True)  # Field name made lowercase.
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    ntt_id = models.AutoField(db_column='NTT_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    ntt_id = models.AutoField(db_column='NTT_ID', primary_key=True)  # Field name made lowercase.
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
    ntt_id = models.BigAutoField(db_column='NTT_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Ciscscv8(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ciscscv8 = models.CharField(db_column='CISCSCv8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'ciscscv8'


class Cobit2019(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cobit2019 = models.CharField(db_column='COBIT2019', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'cobit2019'


class Cosov2017(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cosov2017 = models.CharField(db_column='COSOv2017', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'cosov2017'


class Csaccmv4(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    csaccmv4 = models.CharField(db_column='CSACCMv4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'csaccmv4'


class Csaiotscfv2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    csaiotscfv2 = models.CharField(db_column='CSAIoTSCFv2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'csaiotscfv2'


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
    identifier = models.CharField(db_column='Identifier', primary_key=True, max_length=255)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    security_privacy_by_design_s_p_principles = models.CharField(db_column='Security & Privacy by Design (S|P) Principles', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    principle_intent = models.TextField(db_column='Principle Intent', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'domains'


class Emeaeudora(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emeaeudora = models.CharField(db_column='EMEAEUDORA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'emeaeudora'


class EmeaeueprivacyDraft(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emeaeueprivacy_draft_field = models.CharField(db_column='EMEAEUePrivacy(draft)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'emeaeueprivacy(draft)'


class Emeaeugdpr(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emeaeugdpr = models.CharField(db_column='EMEAEUGDPR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'emeaeugdpr'


class Emeaeupsd2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emeaeupsd2 = models.CharField(db_column='EMEAEUPSD2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'emeaeupsd2'


class Emeaspain(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emeaspain = models.CharField(db_column='EMEASpain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'emeaspain'


class Emeaspainccnstic825(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emeaspainccnstic825 = models.CharField(db_column='EMEASpainCCNSTIC825', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'emeaspainccnstic825'


class Enisav2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enisav2 = models.CharField(db_column='ENISAv2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'enisav2'


class EvidenceRequestCatalog(models.Model):
    evidence_request_references = models.CharField(db_column='Evidence Request References', primary_key=True, max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    area_of_focus = models.CharField(db_column='Area of Focus', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    artifact = models.CharField(db_column='Artifact', max_length=255, blank=True, null=True)  # Field name made lowercase.
    artifact_description = models.TextField(db_column='Artifact Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    control_mappings = models.CharField(db_column='Control Mappings', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'evidence request catalog'


class FrameworkList(models.Model):
    framework_name = models.CharField(db_column='Framework Name', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    table_name = models.CharField(db_column='Table Name', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    framework_id = models.CharField(db_column='Framework ID', primary_key=True, max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    selected = models.IntegerField(db_column='Selected', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'framework list'


class Hipaahicplargepractice(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hipaahicplargepractice = models.CharField(db_column='HIPAAHICPLargePractice', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'hipaahicplargepractice'


class Hipaahicpmediumpractice(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hipaahicpmediumpractice = models.CharField(db_column='HIPAAHICPMediumPractice', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'hipaahicpmediumpractice'


class Hipaahicpsmallpractice(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hipaahicpsmallpractice = models.CharField(db_column='HIPAAHICPSmallPractice', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'hipaahicpsmallpractice'


class Identifydiscretionarysecurityre(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    identifydiscretionarysecurityrequirements_dsr_field = models.CharField(db_column='IdentifyDiscretionarySecurityRequirements(DSR)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'identifydiscretionarysecurityre'


class Identifyminimumcompliancecontro(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    identifyminimumcompliancecontrols_mcc_field = models.CharField(db_column='IdentifyMinimumComplianceControls(MCC)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'identifyminimumcompliancecontro'


class Iec6244342(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iec6244342 = models.CharField(db_column='IEC6244342', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iec6244342'


class Iso27018V2014(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso_27018v2014 = models.CharField(db_column='ISO 27018v2014', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso 27018v2014'


class Iso22301V2019(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso22301v2019 = models.CharField(db_column='ISO22301v2019', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso22301v2019'


class Iso27001V2013(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso27001v2013 = models.CharField(db_column='ISO27001v2013', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso27001v2013'


class Iso27001V2022(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso27001v2022 = models.CharField(db_column='ISO27001v2022', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso27001v2022'


class Iso27002V2013(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso27002v2013 = models.CharField(db_column='ISO27002v2013', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso27002v2013'


class Iso27002V2022(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso27002v2022 = models.CharField(db_column='ISO27002v2022', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso27002v2022'


class Iso27017V2015(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso27017v2015 = models.CharField(db_column='ISO27017v2015', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso27017v2015'


class Iso27701V2019(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso27701_v2019 = models.CharField(db_column='ISO27701 v2019', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso27701 v2019'


class Iso29100V2011(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso29100v2011 = models.CharField(db_column='ISO29100v2011', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso29100v2011'


class Iso31000V2009(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso31000v2009 = models.CharField(db_column='ISO31000v2009', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso31000v2009'


class Iso31010V2009(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iso31010v2009 = models.CharField(db_column='ISO31010v2009', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'iso31010v2009'


class MaturirtyTable(models.Model):
    ccmmcod = models.CharField(db_column='CCMMCOD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sublevels = models.CharField(db_column='SUBLEVELS', primary_key=True, max_length=255)  # Field name made lowercase.
    percentage = models.FloatField(db_column='PERCENTAGE', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'maturirty table'


class Minimumsecurityrequirementsmcc(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minimumsecurityrequirementsmcc_dsr = models.CharField(db_column='MinimumSecurityRequirementsMCC+DSR', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'minimumsecurityrequirementsmcc+'


class Nist800160(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800160 = models.CharField(db_column='NIST800160', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800160'


class Nist800161Rev1(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800161rev1 = models.CharField(db_column='NIST800161rev1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800161rev1'


class Nist800161Rev1Cscrmbaseline(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800161rev1cscrmbaseline = models.CharField(db_column='NIST800161rev1CSCRMBaseline', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800161rev1cscrmbaseline'


class Nist800161Rev1FlowDown(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800161rev1flow_down = models.CharField(db_column='NIST800161rev1Flow Down', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800161rev1flow down'


class Nist800161Rev1Level1(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800161rev1level1 = models.CharField(db_column='NIST800161rev1Level1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800161rev1level1'


class Nist800161Rev1Level2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800161rev1level2 = models.CharField(db_column='NIST800161rev1Level2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800161rev1level2'


class Nist800161Rev1Level3(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800161rev1level3 = models.CharField(db_column='NIST800161rev1Level3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800161rev1level3'


class Nist800171A(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800171a = models.CharField(db_column='NIST800171A', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800171a'


class Nist800171Rev2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800171rev2 = models.CharField(db_column='NIST800171rev2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800171rev2'


class Nist800172(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800172 = models.CharField(db_column='NIST800172', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800172'


class Nist800218V11(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist800218v1_1 = models.CharField(db_column='NIST800218v1_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist800218v1_1'


class Nist80037Rev2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80037rev2 = models.CharField(db_column='NIST80037rev2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80037rev2'


class Nist80039(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80039 = models.CharField(db_column='NIST80039', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80039'


class Nist80053Rev4(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev4 = models.CharField(db_column='NIST80053rev4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev4'


class Nist80053Rev4High(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev4_high_field = models.CharField(db_column='NIST80053rev4(high)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev4(high)'


class Nist80053Rev4Low(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev4_low_field = models.CharField(db_column='NIST80053rev4(low)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev4(low)'


class Nist80053Rev4Moderate(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev4_moderate_field = models.CharField(db_column='NIST80053rev4(moderate)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev4(moderate)'


class Nist80053Rev5(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev5 = models.CharField(db_column='NIST80053rev5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev5'


class Nist80053Rev5High(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev5_high_field = models.CharField(db_column='NIST80053rev5(high)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'nist80053rev5(high)'


class Nist80053Rev5Low(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev5_low_field = models.CharField(db_column='NIST80053rev5(low)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev5(low)'


class Nist80053Rev5Moderate(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev5_moderate_field = models.CharField(db_column='NIST80053rev5(moderate)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev5(moderate)'


class Nist80053Rev5Noc(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev5_noc_field = models.CharField(db_column='NIST80053rev5(NOC)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev5(noc)'


class Nist80053Rev5Privacy(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80053rev5_privacy_field = models.CharField(db_column='NIST80053rev5(privacy)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80053rev5(privacy)'


class Nist80063BPartialmapping(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80063b_partialmapping_field = models.CharField(db_column='NIST80063B(partialmapping)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80063b(partialmapping)'


class Nist80082Rev2Highimpacticsoverl(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80082rev2highimpacticsoverlay = models.CharField(db_column='NIST80082rev2HighImpactICSOverlay', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80082rev2highimpacticsoverl'


class Nist80082Rev2Lowimpacticsoverla(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80082rev2lowimpacticsoverlay = models.CharField(db_column='NIST80082rev2LowImpactICSOverlay', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80082rev2lowimpacticsoverla'


class Nist80082Rev2Moderateimpacticso(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nist80082rev2moderateimpacticsoverlay = models.CharField(db_column='NIST80082rev2ModerateImpactICSOverlay', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nist80082rev2moderateimpacticso'


class Nistarmfai1001V1(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nistarmfai1001v1 = models.CharField(db_column='NISTARMFAI1001v1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nistarmfai1001v1'


class Nistcsfv11(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nistcsfv1_1 = models.CharField(db_column='NISTCSFv1_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nistcsfv1_1'


class Nistprivacyframeworkv1(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nistprivacyframeworkv1 = models.CharField(db_column='NISTPrivacyFrameworkv1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nistprivacyframeworkv1'


class Nistssdf(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nistssdf = models.CharField(db_column='NISTSSDF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nistssdf'


class NttcsCf20231(models.Model):
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)  # Field name made lowercase.
    selected_y_n_field = models.CharField(db_column='Selected? (Y/N)', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    control = models.CharField(db_column='Control', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    control_description = models.CharField(db_column='Control Description', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relative_control_weighting = models.FloatField(db_column='Relative Control Weighting', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    function_grouping = models.CharField(db_column='Function Grouping', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    scrm1 = models.CharField(db_column='SCRM1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scrm2 = models.CharField(db_column='SCRM2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scrm3 = models.CharField(db_column='SCRM3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assesed_result = models.CharField(db_column='Assesed result', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    numeric_result = models.CharField(db_column='Numeric result', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    weighted_numeric_result = models.FloatField(db_column='Weighted Numeric result', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assessment_comments = models.CharField(db_column='Assessment Comments', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relative_result_by_function = models.FloatField(db_column='Relative result by Function', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    relative_result_by_domain = models.FloatField(db_column='Relative result by Domain', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'nttcs cf 2023 1'


class Owasptop10V2021(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    owasptop10v2021 = models.CharField(db_column='OWASPTop10v2021', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'owasptop10v2021'


class Pcidssv32(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pcidssv3_2 = models.CharField(db_column='PCIDSSv3_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'pcidssv3_2'


class Pcidssv40(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pcidssv4_0 = models.CharField(db_column='PCIDSSv4_0', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pcidssv4_0'


class RiskCatalog(models.Model):
    risk_grouping = models.CharField(db_column='Risk Grouping', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    risk_id = models.CharField(db_column='Risk ID', primary_key=True, max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    risk = models.CharField(db_column='Risk', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description_of_possible_risk_due_to_control_deficiency = models.CharField(db_column='Description of Possible Risk Due To Control Deficiency', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    frequency = models.CharField(db_column='Frequency', max_length=255, blank=True, null=True)  # Field name made lowercase.
    freqnum = models.FloatField(db_column='FreqNum', blank=True, null=True)  # Field name made lowercase.
    impact = models.CharField(db_column='Impact', max_length=255, blank=True, null=True)  # Field name made lowercase.
    impactnum = models.FloatField(db_column='ImpactNum', blank=True, null=True)  # Field name made lowercase.
    risk_val = models.FloatField(db_column='Risk Val', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    function = models.CharField(db_column='Function', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'risk catalog'


class ScfbbusinessmergersAcquisition(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scfbbusinessmergers_acquisitions = models.CharField(db_column='SCFBBusinessMergers&Acquisitions', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'scfbbusinessmergers&acquisition'


class Scfeembeddedtechnology(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scfeembeddedtechnology = models.CharField(db_column='SCFEEmbeddedTechnology', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'scfeembeddedtechnology'


class Scficyberinsurance(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scficyberinsurance = models.CharField(db_column='SCFICyberInsurance', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'scficyberinsurance'


class Scfrransomwareprotection(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scfrransomwareprotection = models.CharField(db_column='SCFRRansomwareProtection', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'scfrransomwareprotection'


class ThreatCatalog(models.Model):
    threat_group = models.CharField(db_column='Threat Group', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    threat_id = models.CharField(db_column='Threat ID', primary_key=True, max_length=255)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    threat = models.CharField(db_column='Threat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    threat_description = models.TextField(db_column='Threat Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'threat catalog'


class Usc2M2V21(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    usc2m2v2_1 = models.CharField(db_column='USC2M2v2_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'usc2m2v2_1'


class Uscertrmmv12(models.Model):
    idntt_id = models.CharField(db_column='IDNTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uscertrmmv1_2 = models.CharField(db_column='USCERTRMMv1_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'uscertrmmv1_2'


class Uscmmc20Level1(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uscmmc2_0level_1 = models.CharField(db_column='USCMMC2_0Level 1', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'uscmmc2_0level 1'


class Uscmmc20Level2(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uscmmc2_0level2 = models.CharField(db_column='USCMMC2_0Level2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'uscmmc2_0level2'


class Uscmmc20Level3(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uscmmc2_0level3 = models.CharField(db_column='USCMMC2_0Level3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'uscmmc2_0level3'


class Ushipaa(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ushipaa = models.CharField(db_column='USHIPAA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'ushipaa'


class Ussox(models.Model):
    ntt_id = models.CharField(db_column='NTT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ussox = models.CharField(db_column='USSOX', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        managed = False
        db_table = 'ussox'


class SeleccionAssessment(models.Model):
    seleccion = models.CharField( max_length=255, blank=True, null=True)
    valor = models.CharField( max_length=255, blank=True, null=True)
    objects = models.Manager()