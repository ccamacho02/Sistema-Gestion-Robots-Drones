from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Devices
from .forms import ReservaForm, GrabacionForm, EntregaForm

def reservar(request):
    if request.method == 'POST':
        reserva_form = ReservaForm(request.POST)
        grabacion_form = GrabacionForm(request.POST)
        entrega_form = EntregaForm(request.POST)

        if reserva_form.is_valid():
            reserva_instance = reserva_form.save(commit=False)
            tipo_servicio = reserva_instance.tipo_servicio

            if tipo_servicio == 'Grabacion' and grabacion_form.is_valid():
                reserva_instance.lugar_evento = grabacion_form.cleaned_data['lugar_evento']
                reserva_instance.lugar_grabacion = grabacion_form.cleaned_data['lugar_grabacion']
                reserva_instance.duracion_evento = grabacion_form.cleaned_data['duracion_evento']
                reserva_instance.save()
                return redirect('index')  # Redirigir a una página de éxito
            elif tipo_servicio == 'Entrega' and entrega_form.is_valid():
                reserva_instance.lugar_origen = entrega_form.cleaned_data['lugar_origen']
                reserva_instance.lugar_destino = entrega_form.cleaned_data['lugar_destino']
                reserva_instance.medidas_paquete = entrega_form.cleaned_data['medidas_paquete']
                reserva_instance.peso_paquete = entrega_form.cleaned_data['peso_paquete']
                reserva_instance.correo_destinatario = entrega_form.cleaned_data['correo_destinatario']
                reserva_instance.save()
                return redirect('index')  # Redirigir a una página de éxito
    else:
        reserva_form = ReservaForm()
        grabacion_form = GrabacionForm()
        entrega_form = EntregaForm()

    return render(request, 'reservar.html', {
        'reserva_form': reserva_form,
        'grabacion_form': grabacion_form,
        'entrega_form': entrega_form,
    })

def notify_low_stock():
   subject = 'Codigo QR confirmacion de reserva'
   message = 'A coontinuación, está el código QR para que pueda confirmar la entrega de su producto:'
   template = render_to_string('email.html', {
      'message': message,
      'product': 'codigo QR',
   })

   email_user = EmailMessage(
      subject,
      template,
      settings.EMAIL_HOST_USER,
      ['carloscamacho0602@gmail.com']
   )
   
   email_admin = EmailMessage(
      subject,
      template,
      settings.EMAIL_HOST_USER,
      ['sistema.gestion.drones@gmail.com']
   )

   email_user.fail_silently = False
   email_admin.fail_silently = False
   email_user.send()
   email_admin.send()

def agendar_reserva(request):
   # if request.method == 'POST':
   #    notify_low_stock()
   #    return redirect('agendar_reserva')
   notify_low_stock()
   return render(request, 'agendar_reserva.html')

def inventario(request):
   devices = Devices.objects.all()
   if devices:
      return render(request,'inventario.html',{
         'devices': devices,
      })
   else:
      return render(request,'inventario.html',{
         'error': 'No hay dispositivos en el momento',
      })