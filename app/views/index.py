from django.shortcuts import redirect, render

from app.models import Usuarios
from django.contrib.auth import authenticate, login, logout
import random
import string
import smtplib
from django.db.models import Q
from django.conf import settings
from email.message import EmailMessage

import importlib
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):
    # Importa el módulo de forma dinámica
    formulario_module = importlib.import_module('app.views.formulario')
    
    context = {
        # Verifica si el usuario tiene rol admin
        "is_admin": formulario_module.user_has_role(request.user, 'Admin')
    }
    return render(request, 'index.html', context)


def login_(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Usuarios.objects.filter(Q(email=email)).first()
            if not usuario.is_active and password==usuario.temp_password:
                return activate_user(request, usuario, password)

            user = authenticate(request, username=usuario, password=password)
            if user is not None:
                login(request, user)
                return redirect(index)
            else:
                msg = 'Datos incorrectos, intente de nuevo'
                return render(request, 'login/login.html', {'msg':msg})
        except:
            msg = 'Datos incorrectos, intente de nuevo'
            return render(request, 'login/login.html', {'msg':msg})
    else:
        return render(request, 'login/login.html')
    
def logout_(request):
    logout(request)
    return redirect(index)

def activate_user(request, usuario, password):
    if request.POST['newpassword'] == 'True':
        return render(request, 'login/activateUser.html', {'password':password, 'email':usuario.email})
    else:
        usuario.set_password(request.POST['newpassword'])
        usuario.is_active = True
        usuario.temp_password = ''
        usuario.save()
        return redirect(login_)

def recover_password(request):
    email = request.POST.get('email')
    if request.method == 'POST':
        if Usuarios.objects.filter(email=email).exists():
            receiver_email_address = email
            email_subject = "Recupera tu contraseña"

            comp = Usuarios.objects.get(email=request.POST["email"])
            password = generar_password()
            comp.temp_password = password
            comp.is_active = False
            comp.save()

            print(sendEmail(email_subject, receiver_email_address, "Cordial saludo, al parecer usted ha perdido el acceso a nuestra plataforma, este es su contraseña temporal: " + password))

            request.session['msg'] = "Se envio su nueva contraseña via correo, revise su bandeja"  # noqa: E501
            return redirect(login_)
        else:
            msg = "Este email no esta registrado a nuestra pagina"
        return render(request, "login/recoverPassword.html", {'msg':msg})
    else:
        return render(request, "login/recoverPassword.html")
    
def generar_password(longitud=8):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres)
                    for i in range(longitud))
    return password

def sendEmail(subject: str, receiverEmail: str, content: str) -> bool:
    try:
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = settings.SENDER_EMAIL_ADDRESS
        message['To'] = receiverEmail
        message.set_content(content)
        server = smtplib.SMTP(settings.STMPURL, '587')
        server.ehlo()
        server.starttls()
        server.login(settings.SENDER_EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()
        return True
    except:
        return False