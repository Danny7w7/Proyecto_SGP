import random
import string
import smtplib

from email.message import EmailMessage

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
from functools import wraps

from app.forms import ProyectoForm
from app.models import Usuarios, Autores, Codigos_grupo_investigacion, Nombre_grupo_investigacion, Redes_conocimiento, Subareas_conocimiento, Diciplina_subarea, Proyecto
from django.contrib.auth.decorators import login_required
def register(request):
    if request.method == 'POST':
        if Usuarios.objects.filter(email=request.POST["email"]).exists():
            msg = "Este email ya existe"
            return render(request, 'login/register.html', {'msg': msg})
        else:
            afterhashed = request.POST["password"]
            user = Usuarios.objects.create_user(email=request.POST["email"],
                                            password=request.POST["password"],
                                            username=request.POST["email"],
                                            first_name=request.POST["first_name"],
                                            last_name=request.POST["last_name"],
                                            tipo_documento=request.POST["tipo_documento"],
                                            num_documento=request.POST["num_documento"])
            user.save()
            userl = authenticate(
                request, username=user.username, password=afterhashed)
            login(request, userl)
            return redirect(index)
    else:
        return render(request, 'login/register.html')


def login_(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
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

            request.session['msg'] = "Se envio su nueva contraseña via correo, revise su bandeja"
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
    
def edit_proyect(request):
    user = request.user
    proyecto = user.proyecto_set.first()
    print(proyecto)
    if request.method == 'POST':
        #Aqui se va a obtener el proyecto asociado al usuario (Cuando Cova termine la asociacion :v)

        model = Proyecto
        column_names = [field.name for field in model._meta.fields]
        
        for name in column_names:
            if name == 'id' or name == 'usuario':
                continue
            print(request.POST.get(name))
            print("Guardo"+name+"\n")
            setattr(proyecto, name, request.POST.get(name))
        proyecto.save()

    context = {'proyecto':user.proyecto_set.first(),
            'listaPlegable':contex_form()}
    return render(request, 'edit_form/edit_proy.html', context)

def index(request):
    return render(request, 'index.html')

def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)

@login_required(login_url='/login')   
def crear_proyecto(request):
    # Validacion que permita solo admin y formulador
    if user_has_role(request.user, 'Admin', 'F'):
        if request.method == "POST":
            form = ProyectoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('info_proyecto')
        else:
            form = ProyectoForm()

        context = {'form': form,
               'listaPlegable':contex_form()}
        return render(request, 'form/crearp.html', context)
    
    return redirect('index')

def contex_form():
    codigos = Codigos_grupo_investigacion.objects.all().order_by('codigo')
    nombres = Nombre_grupo_investigacion.objects.all().order_by('nombre')
    redes = Redes_conocimiento.objects.all().order_by('nombre')
    subareas = Subareas_conocimiento.objects.all().order_by('nombre')
    diciplinas = Diciplina_subarea.objects.all().order_by('nombre')
    return {'codigos':codigos,
            'nombres':nombres,
            'redes':redes,
            'subareas':subareas,
            'diciplinas':diciplinas}

  
#Funciones de ADMIN MENU
def admin(request):
    return render(request, 'Dashboard/Admin.html')

def not404(request):
    return render(request, 'Dashboard/404.html')

def anexosdoc(request):
    return render(request, 'Dashboard/Anexos.html')

def usuarios(request):
    return render(request, 'Dashboard/Eliminar.html')

def preguntas(request):
    return render(request, 'Dashboard/PreguntasP.html')

def proyectosINA(request):
    return render(request, 'Dashboard/Proyectos-eliminados.html')

def proyectoP(request):
    return render(request, 'Dashboard/Proyectos-pendientes.html')

def proyectoT(request):
    return render(request, 'Dashboard/Proyectos-terminado.html')