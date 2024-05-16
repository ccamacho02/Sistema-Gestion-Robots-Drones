from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm, OTPForm
from .utils import send_otp
from datetime import datetime
import pyotp


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
        password = request.POST['password']
        user = authenticate(
            request, username=username, password=password)

        if user is None:
            return render(request, 'signin.html', {
                'form': CustomAuthenticationForm,
                'error': 'Usuario o Contraseña Incorrectos',
            })
        else:
            request.session['username'] = username
            send_otp(request)
            return redirect('otp')
        
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
