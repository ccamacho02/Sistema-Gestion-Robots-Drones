from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm, OTPForm
from .utils import send_otp
from datetime import datetime
import pyotp
from django.contrib.auth.decorators import login_required


def obligatory(request):
    return redirect('signin')

def index(request):
        return render(request,'index.html')
        
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })

@login_required
def signout(request):
    logout(request)
    return redirect('index')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': CustomAuthenticationForm,
        })
    else:
        username = request.POST['username']
        try:
            username = User.objects.get(email=username).username
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            user = None

        if user is None:
            return render(request, 'signin.html', {
                'form': CustomAuthenticationForm,
                'error': 'Usuario o Contraseña Incorrectos',
            })
        else:
            request.session['username'] = username
            otp = send_otp(request)
            enviar_otp(otp)
            return redirect('otp')
        
def enviar_otp(otp):
    subject = 'Codigo de verificación de dos pasos'
    message = 'Su código de verificación de dos pasos para que pueda iniciar sesión en su cuenta es:'
    template = render_to_string('email_otp.html', {
        'message': message,
        'otp': otp,
    })

    email_admin = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        ['sistema.gestion.drones@gmail.com']
    )

    email_admin.fail_silently = False
    email_admin.send()
        
def otp(request):
    form = OTPForm()
    error_message = ''
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_until']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_until']
                    return redirect('index')
                else:
                    error_message = 'Invalid OTP'
            else:
                error_message = 'OTP Expired'
        else:
            error_message = 'OTP not sent'
    return render(request, 'otp.html', {'error': error_message, 'form': form})

