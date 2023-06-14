from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('assessment/', views.assessment),
    path('assessmentselect/', views.assessmentselect),
    path('exportaciones/', views.Exportaciones),
    path('informes/', views.informes),
    path('mantenimiento/', views.Mantenimiento),
    path('menu/', views.menu),
]

