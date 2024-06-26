# Generated by Django 5.0.2 on 2024-05-16 22:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispositivo', models.CharField(help_text='Ingrese el nombre del dispositivo', max_length=100, unique=True, verbose_name='Nombre del dispositivo')),
                ('cantidad', models.IntegerField(default=1, help_text='Ingrese la cantidad de dispositivos disponibles', verbose_name='Cantidad de dispositivos')),
                ('estado', models.CharField(choices=[('Disponible', 'Disponible'), ('No Disponible', 'No Disponible'), ('En mantenimiento', 'En mantenimiento')], help_text='Seleccione el estado del dispositivo', max_length=50, verbose_name='Estado del dispositivo')),
                ('tipo', models.CharField(choices=[('Robot', 'Robot'), ('Drone', 'Drone'), ('Sensor', 'Sensor'), ('Otro', 'Otro')], help_text='Seleccione el tipo de dispositivo', max_length=50, verbose_name='Tipo de dispositivo')),
                ('marca', models.CharField(blank=True, help_text='Ingrese la marca del dispositivo (opcional)', max_length=100, null=True, verbose_name='Marca del dispositivo')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100)),
                ('correo_institucional', models.EmailField(max_length=254)),
                ('tipo_identificacion', models.CharField(choices=[('CC', 'C.C'), ('TI', 'T.I')], max_length=50)),
                ('numero_identificacion', models.CharField(max_length=50)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('hora', models.TimeField(default=datetime.time(8, 0))),
                ('tipo_servicio', models.CharField(choices=[('Grabacion', 'Grabación'), ('Entrega', 'Entrega')], max_length=20)),
                ('lugar_evento', models.CharField(blank=True, choices=[('1', 'Lugar 1'), ('2', 'Lugar 2'), ('3', 'Lugar 3')], max_length=50, null=True)),
                ('lugar_grabacion', models.CharField(blank=True, choices=[('1', 'Lugar 1'), ('2', 'Lugar 2'), ('3', 'Lugar 3')], max_length=50, null=True)),
                ('duracion_evento', models.DurationField(blank=True, default=datetime.timedelta(seconds=3600), null=True)),
                ('lugar_origen', models.CharField(blank=True, choices=[('1', 'Lugar 1'), ('2', 'Lugar 2'), ('3', 'Lugar 3')], max_length=100, null=True)),
                ('lugar_destino', models.CharField(blank=True, choices=[('1', 'Lugar 1'), ('2', 'Lugar 2'), ('3', 'Lugar 3')], max_length=100, null=True)),
                ('medidas_paquete', models.CharField(blank=True, max_length=50, null=True)),
                ('peso_paquete', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('correo_destinatario', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]
