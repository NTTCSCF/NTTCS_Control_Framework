from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index.as_view(), name='login'),
    path('accounts/login/', views.index.as_view(), name='login'),
    path('menu/', views.menu.as_view(), name='menu'),
    path('assessment/', views.assessment.as_view(), name='assessment'),
    path('assessmentselect/', views.assessmentselect.as_view(), name='assessmentselect'),
    path('exportaciones/', views.Exportaciones.as_view(), name='exportaciones'),
    path('informes/', views.informes.as_view(), name='informes'),
    path('mantenimiento/', views.Mantenimiento.as_view(), name='mantenimiento'),
    path('menu/', views.menu.as_view(), name='menu'),
    path('usuarios/', views.Usuarios.as_view(), name='usuarios'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),
    path('creacionPass/', views.CreacionPass.as_view(), name='creacionPass'),
    path('mantenimientoNivelMadurez/', views.MantenimientoNivelMadurez.as_view(), name='mantenimientoNivelMadurez'),
    path('mantenimientoNivelMadurez/Eliminar/', views.MantenimientoNivelMadurez.Eliminar, name='Eliminar'),
    path('MantenimientoDominios/', views.MantenimientoDominios.as_view(), name='MantenimientoDominios'),
    path('mantenimientoDominios/Eliminar/', views.MantenimientoDominios.Eliminar, name='EliminarDominios'),
    path('MantenimientoEvidencias/', views.MantenimientoEvidencias.as_view(), name='MantenimientoEvidencias'),
    path('mantenimientoEvidencias/Eliminar/', views.MantenimientoEvidencias.Eliminar, name='EliminarEvidencias'),
    path('MantenimientoPreguntas/', views.MantenimientoPreguntas.as_view(), name='MantenimientoPreguntas'),
    path('mantenimientoPreguntas/Eliminar/', views.MantenimientoPreguntas.Eliminar, name='EliminarPreguntas'),
    path('MantenimientoMarcosExistentes/', views.MantenimientoMarcosExistentes.as_view(), name='MantenimientoMarcosExistentes'),
    path('MantenimientoMarcosExistentes/Eliminar/', views.MantenimientoMarcosExistentes.Eliminar, name='EliminarMarcos'),
    path('MantenimientoControlesNTTCS/', views.MantenimientoControlesNTTCS.as_view(), name='MantenimientoControlesNTTCS'),
    path('MantenimientoControlesNTTCS/Eliminar/', views.MantenimientoControlesNTTCS.Eliminar, name='EliminarControles'),
    path('MantenimientoMapeoMarcos/', views.MantenimientoMapeoMarcos.as_view(), name='MantenimientoMapeoMarcos'),

    path('MantenimientoAssessmentArchivados/', views.MantenimientoAssessmentArchivados.as_view(), name='MantenimientoAssessmentArchivados'),
    path('MantenimientoAssessmentArchivados/EliminarAssessment/', views.MantenimientoAssessmentArchivados.EliminarAssessment, name='EliminarAssessment'),
    path('logout', views.logout, name='logout'),
    #prueba jose
    path('MantDominios2/', views.MantDominios2.as_view(), name='MantDominios2'),
    path('MantDom3/', views.MantDom3.as_view(), name='MantDom3'),

]


