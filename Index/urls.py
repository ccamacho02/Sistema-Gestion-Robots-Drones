from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('otp/', views.otp, name='otp'),
    path('scan-qr/', views.scan_qr, name='scan-qr'),
    path('capture-qr/', views.capture_qr, name='capture-qr')
]