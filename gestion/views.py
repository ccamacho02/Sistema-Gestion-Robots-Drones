from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

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