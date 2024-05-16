# Generated by Django 5.0.2 on 2024-05-16 17:59

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
    ]
