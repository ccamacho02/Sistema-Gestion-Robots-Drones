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

"""
Opciones de la tabla Devices (Dispositivos)
"""
ESTADO_CHOICES = (
    ('Disponible', 'Disponible'),
    ('No Disponible', 'No Disponible'),
    ('En mantenimiento', 'En mantenimiento'),
)

TIPO_CHOICES = (
    ('Robot', 'Robot'),
    ('Drone', 'Drone'),
    ('Sensor', 'Sensor'),
    ('Otro', 'Otro'),
)

class Devices(models.Model):
    dispositivo = models.CharField(
        verbose_name="Nombre del dispositivo", max_length=100,
        help_text="Ingrese el nombre del dispositivo",unique=True,
        ) 
    cantidad = models.IntegerField(
        verbose_name="Cantidad de dispositivos",
        help_text="Ingrese la cantidad de dispositivos disponibles",
        default=1,
        )
    estado = models.CharField(
        max_length=50, 
        verbose_name="Estado del dispositivo", 
        help_text="Seleccione el estado del dispositivo",
        choices=ESTADO_CHOICES,
        )
    tipo =  models.CharField(
        max_length=50,
        verbose_name="Tipo de dispositivo",
        choices=TIPO_CHOICES,
        help_text="Seleccione el tipo de dispositivo",
        )
    marca = models.CharField(
        max_length=100,
        verbose_name="Marca del dispositivo",
        blank=True,
        null=True,
        help_text="Ingrese la marca del dispositivo (opcional)",
        )
    def __str__(self):
        return self.dispositivo 
