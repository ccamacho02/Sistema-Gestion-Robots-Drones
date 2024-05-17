from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('otp/', views.otp, name='otp'),
]

urlpatterns += [
    re_path(r'^accounts/', views.obligatory, name="obligatory"),
]