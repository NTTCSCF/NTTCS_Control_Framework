from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('', views.assessment),
    path('', views.assessmentselect),
    path('', views.Exportaciones),
    path('', views.informes),
    path('', views.Mantenimiento),
    path('', views.menu),
]

