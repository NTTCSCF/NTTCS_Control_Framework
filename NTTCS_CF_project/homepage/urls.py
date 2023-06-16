from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('assessment/', views.assessment,name='assessment'),
    path('assessmentselect/', views.assessmentselect,name='assessmentselect'),
    path('exportaciones/', views.Exportaciones,name='exportaciones'),
    path('informes/', views.informes,name='informes'),
    path('mantenimiento/', views.Mantenimiento,name='mantenimiento'),
    path('menu/', views.menu,name='menu'),
]

