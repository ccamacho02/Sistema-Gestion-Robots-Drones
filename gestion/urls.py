from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.reservar, name='reservar'),
    path('inventario/', views.inventario, name='inventario'),
    path('scan-qr/', views.scan_qr, name='scan-qr'),
    path('capture-qr/', views.capture_qr, name='capture-qr'),
]
