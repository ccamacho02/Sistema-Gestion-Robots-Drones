from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .models import Devices, Users
from .forms import ReservaForm, GrabacionForm, EntregaForm
from pyzbar import pyzbar
import cv2
import qrcode
import os

import random
import string


def reservar(request):
    if request.method == 'POST':
        reserva_form = ReservaForm(request.POST)
        grabacion_form = GrabacionForm(request.POST)
        entrega_form = EntregaForm(request.POST)

        if reserva_form.is_valid():
            reserva_instance = reserva_form.save(commit=False)
            tipo_servicio = reserva_instance.tipo_servicio
            data_to_encode = generate_random_code()
            qr_code = generate_qr_code(data_to_encode)
            if tipo_servicio == 'Grabacion' and grabacion_form.is_valid():
                reserva_instance.lugar_evento = grabacion_form.cleaned_data['lugar_evento']
                reserva_instance.lugar_grabacion = grabacion_form.cleaned_data['lugar_grabacion']
                reserva_instance.duracion_evento = grabacion_form.cleaned_data['duracion_evento']
                reserva_instance.save()
                enviar_qr(qr_code)
                return redirect('index')  # Redirigir a una página de éxito
            elif tipo_servicio == 'Entrega' and entrega_form.is_valid():
                reserva_instance.lugar_origen = entrega_form.cleaned_data['lugar_origen']
                reserva_instance.lugar_destino = entrega_form.cleaned_data['lugar_destino']
                reserva_instance.medidas_paquete = entrega_form.cleaned_data['medidas_paquete']
                reserva_instance.peso_paquete = entrega_form.cleaned_data['peso_paquete']
                reserva_instance.correo_destinatario = entrega_form.cleaned_data[
                    'correo_destinatario']
                reserva_instance.save()
                enviar_qr(qr_code)
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


def enviar_qr(qr_code):
    subject = 'Codigo QR confirmacion de reserva'
    message = 'A continuación, adjuntamos el código QR para que pueda confirmar la entrega de su producto:'
    template = render_to_string('email.html', {
        'message': message,
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
    with open(qr_code, 'rb') as img:
        image = img.read()
        email_user.attach('qr_code.png', image, 'image/png')
        email_admin.attach('qr_code.png', image, 'image/png')
    email_user.send()
    email_admin.send()



def generate_qr_code(data, filename='qr_code.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join(settings.BASE_DIR, 'media', filename)
    img.save(img_path)
    return img_path


def generate_random_code(length=10):
    # Define el conjunto de caracteres: letras mayúsculas y números
    characters = string.ascii_uppercase + string.digits
    # Genera un código aleatorio
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code



def inventario(request):
    devices = Devices.objects.all()
    if devices:
        return render(request, 'inventario.html', {
            'devices': devices,
        })
    else:
        return render(request, 'inventario.html', {
            'error': 'No hay dispositivos en el momento',
        })


def scan_qr(request):
    return render(request, 'scan_qr.html')


def capture_qr(request):
    barcodeData = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '')
        user = Users.objects.filter(codigo=codigo)
        print(user)
        if user.exists():
            name = user[0].nombre
            messages.success(request, f'El usuario con codigo {codigo} es {name}')
            return redirect('reservar')
        else:
            messages.error(request, f'El usuario con codigo {codigo} no existe')
            return redirect('scan-qr')
    else:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    print("Barcode: {} - Type: {}".format(barcodeData, barcodeType))

                cv2.imshow("Barcode Scanner", frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            else:
                break
        return render(request, 'scan_qr.html', {'qr_result': barcodeData})
