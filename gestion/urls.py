from django.urls import path
from . import views

urlpatterns = [
    path('notification', views.agendar_reserva, name='notification'),
    path('reservar/', views.reservar, name='reservar'),
    path('inventario/', views.inventario, name='inventario'),
]
