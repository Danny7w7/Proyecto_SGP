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

from app.forms import AutoresForm, ParticipantesForm, ProyectoForm, Informacion_de_centroForm, Informacion_ProyectoForm, Estructura_del_proyectoForm, Analisis_ParticipantesForm, Entidades_aliadasForm, RiesgoObjetivoGeneralForm, RiesgoProductosForm, RiesgoActividadesForm, Estructura_arbol_problemasForm, Estructura_problemaForm
from app.models import Usuarios, Autores, Participantes_Proyecto, Proyecto

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

def index(request):
    print("UwU")
    return render(request, 'index.html')

def user_has_role(*required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Comprobar primero si el usuario está autenticado
            if not request.user.is_authenticated:
                return redirect('login') 
            # Si está autenticado, verifica los roles
            
            if not request.user.roles.filter(rol__in=required_roles).exists():
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@user_has_role('Admin', 'F')
def crear_proyecto(request):
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('info_proyecto')
        
    else:
        form = ProyectoForm()

    context = {'form': form}
    return render(request, 'form/crearp.html', context)

# Informacion proponente
def Informacion_de_centro_view(request):
    if request.method == "POST":
        form = Informacion_de_centroForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Informacion_de_centroForm()
    
    context = {'form': form}
    return render(request, 'form/infop.html', context)

def  Autores_view(request):
    if request.method == "POST":
        form = AutoresForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AutoresForm()
    
    context = {'form': form}
    return render(request, 'form/infop.html', context)

# Mostrar info de autores
def Mostrar_autores(request):
    m_autores = Autores.objects.all()  # obtiene todos los registros del modelo
    return render(request, 'form/infop.html', {'m_autores': m_autores})

def  Participantes_view(request):
    if request.method == "POST":
        form = ParticipantesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ParticipantesForm()
    
    context = {'form': form}
    return render(request, 'form/infop.html', context)


#---------------------- Pruebas ---------------#

# def Autores_view(request):
#     if request.method == 'POST':
#         autor_formset = AutorFormSet(request.POST, prefix='autor')


#         if autor_formset.is_valid():
            
#             pass

#     else:
#         autor_formset = AutorFormSet(queryset=Autores.none(), prefix='autor')
    
#         return render(request, 'infop.html', {
#         'autor_formset': autor_formset
#     })
        

# def Participantes_view(request):
#     if request.method == 'POST':
#         participante_formset = ParticipanteFormSet(request.POST, prefix='participante')

#         if participante_formset.is_valid():
           
#             pass

#     else:
#         participante_formset = ParticipanteFormSet(queryset=Participantes_Proyecto.none(), prefix='participante')

#     return render(request, 'infop.html', {
#         'participante_formset': participante_formset
#     })


def  Informacion_Proyecto_view(request):
    if request.method == "POST":
        form = Informacion_ProyectoForm(request.POST)
        # print(form.erros)
        if form.is_valid():
            form.save()
    else:
        form = Informacion_ProyectoForm()
    
    context = {'form': form}
    return render(request, 'form/infop.html', context)

def  Estructura_del_proyecto_view(request):
    if request.method == "POST":
        form = Estructura_del_proyectoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Estructura_del_proyectoForm()
    
    context = {'form': form}
    return render(request, 'form/estp.html', context)
    
def  Estructura_arbol_problemas_view(request):
    if request.method == "POST":
        form = Estructura_arbol_problemasForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Estructura_arbol_problemasForm()
    
    context = {'form': form}
    return render(request, 'form/estp.html', context)

def  Estructura_problema_view(request):
    if request.method == "POST":
        form = Estructura_problemaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Estructura_problemaForm()
    
    context = {'form': form}
    return render(request, 'form/estp.html', context)

def  Analisis_Participantes_view(request):
    if request.method == "POST":
        form = Analisis_ParticipantesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Analisis_ParticipantesForm()
    
    context = {'form': form}
    return render(request, 'form/partp.html', context)

def  Entidades_aliadas_view(request):
    if request.method == "POST":
        form = Entidades_aliadasForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Entidades_aliadasForm()
    
    context = {'form': form}
    return render(request, 'form/partp.html', context)

def Riesgos_objetivo_general_view(request):
    if request.method == 'POST':
        form = RiesgoObjetivoGeneralForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RiesgoObjetivoGeneralForm()

    context = {'form': form}
    return render(request, 'form/riesgosp.html', context)

def Riesgo_productos_view(request):
    if request.method == 'POST':
        form = RiesgoProductosForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RiesgoProductosForm()

    context = {'form': form}
    return render(request, 'form/riesgosp.html', context)

def Riesgo_actividades_view(request):
    if request.method == 'POST':
        form = RiesgoActividadesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RiesgoActividadesForm()

    context = {'form': form}
    return render(request, 'form/riesgosp.html', context)

def Metodologia_view(request):
    return render(request, 'form/metodologia.html')

def Objetivos_view(request):
    return render(request, 'form/objetivos.html')

def Anexos_view(request):
    return render(request, 'form/anexos.html')

def Proyeccion_view(request):
    return render(request, 'form/proyeccion.html')
  
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