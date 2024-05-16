from django.db import models

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
