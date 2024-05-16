from django.db import models
from datetime import date, time, timedelta

TIPO_SERVICIO_CHOICES = (
        ('Grabacion', 'Grabación'),
        ('Entrega', 'Entrega'),
)

TIPO_IDENTIFICACION_CHOICES = (
        ('CC', 'C.C'),
        ('TI', 'T.I')
)

LUGAR_CHOICES = (
        ('1', 'Lugar 1'),
        ('2', 'Lugar 2'),
        ('3', 'Lugar 3'),
)

class Reserva(models.Model):

    nombre_completo = models.CharField(max_length=100)
    correo_institucional = models.EmailField()
    tipo_identificacion = models.CharField(max_length=50, choices=TIPO_IDENTIFICACION_CHOICES)
    numero_identificacion = models.CharField(max_length=50)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=time(hour=8, minute=0))
    tipo_servicio = models.CharField(max_length=20, choices=TIPO_SERVICIO_CHOICES)
    lugar_evento = models.CharField(max_length=50, blank=True, null=True, choices=LUGAR_CHOICES)
    lugar_grabacion = models.CharField(max_length=50, blank=True, null=True, choices=LUGAR_CHOICES)
    duracion_evento = models.DurationField(blank=True, null=True, default=timedelta(hours=1))
    lugar_origen = models.CharField(max_length=100, blank=True, null=True, choices=LUGAR_CHOICES)
    lugar_destino = models.CharField(max_length=100, blank=True, null=True, choices=LUGAR_CHOICES)
    medidas_paquete = models.CharField(max_length=50, blank=True, null=True)
    peso_paquete = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    correo_destinatario = models.EmailField(blank=True, null=True)
