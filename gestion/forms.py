from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_completo', 'correo_institucional', 'tipo_identificacion', 'numero_identificacion', 'fecha', 'hora', 'tipo_servicio']

class GrabacionForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['lugar_evento', 'lugar_grabacion', 'duracion_evento']

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['lugar_origen', 'lugar_destino', 'medidas_paquete', 'peso_paquete', 'correo_destinatario']
