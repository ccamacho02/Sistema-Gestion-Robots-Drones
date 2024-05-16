from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm, OTPForm
from .utils import send_otp, updateQRResult
from datetime import datetime
from pyzbar import pyzbar
import pyotp
import cv2


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

def scan_qr(request):
    post = False
    return render(request, 'scan_qr.html', {'post': post})

def capture_qr(request):
    if request.method == 'POST':
        pass
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
                    (x, y , w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    print("Barcode: {} - Type: {}".format(barcodeData, barcodeType))

                    #qr_result = updateQRResult(barcodeData)
                
                cv2.imshow("Barcode Scanner", frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    post = True
                    break
            else:
                break
        return render(request, 'scan_qr.html', {'qr_result': barcodeData, 'post': post})
