from django.shortcuts import render, redirect
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
