from django.shortcuts import redirect, render

from app.models import Roles, Usuarios
from django.contrib.auth import authenticate, login, logout
import random
import string
import smtplib
from django.db.models import Q
from django.conf import settings
from email.message import EmailMessage

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        if Usuarios.objects.filter(email=request.POST["email"]).exists():
            msg = "Este email ya existe"
            return render(request, 'login/register.html', {'msg': msg})
        else:
            afterhashed = request.POST["password"]
            try:
                user = Usuarios.objects.create_user(email=request.POST["email"],
                                                password=request.POST["password"],
                                                username=request.POST["email"],
                                                first_name=request.POST["first_name"],
                                                last_name=request.POST["last_name"],
                                                tipo_documento=request.POST["tipo_documento"],
                                                num_documento=request.POST["num_documento"])
                rol_lector = Roles.objects.get(rol='L')
                user.roles.add(rol_lector)
                user.save()
                userl = authenticate(
                    request, username=user.username, password=afterhashed)
                login(request, userl)
                return redirect(index)
            except:
                msg = "Por favor selecciona tu tipo de documento correctamente"
                return render(request, 'login/register.html', {'msg':msg})
    else:
        return render(request, 'login/register.html')


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

            print(sendEmail(email_subject, receiver_email_address, "Hola caballero, al parecer usted ha perdido el acceso a nuestra pagina web, este es su contraseña temporal: " + password))

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