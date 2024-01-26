#Funciones de ADMIN MENU
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.models import Listas_plegables, Usuarios, Roles
from django.contrib.auth.decorators import login_required

from app.views.formulario import get_or_none


def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)


@login_required(login_url='/login')
def admin(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Admin.html')


@login_required(login_url='/login')
def usuarios(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    usuarios = Usuarios.objects.all()
    roles = Roles.objects.all()
    if request.method == 'POST':
        nuevos_roles = request.POST.getlist('roles')
        usuario = Usuarios.objects.get(id=request.POST['id_usuario'])
        usuario.roles.set(Roles.objects.filter(rol__in=nuevos_roles))
    
    return render(request, 'Dashboard/Eliminar.html', {'usuarios': usuarios, 'roles': roles})


@login_required(login_url=('/login'))
def preguntas(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/PreguntasP.html')

@login_required(login_url=('/login'))
def proyectosINA(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Proyectos-eliminados.html')

@login_required(login_url=('/login'))
def proyectoP(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Proyectos-pendientes.html')

@login_required(login_url=('/login'))
def proyectoT(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Proyectos-terminado.html')


@login_required(login_url=('/login'))
def register(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    if request.method == 'POST':
        if Usuarios.objects.filter(email=request.POST["email"]).exists():
            msg = "Este email ya existe"
            return render(request, 'Dashboard/register.html', {'msg': msg})
        else:
            user = Usuarios.objects.create_user(email=request.POST["email"],
                                            password=request.POST["password"],
                                            username=request.POST["email"],
                                            first_name=request.POST["first_name"],
                                            last_name=request.POST["last_name"],
                                            tipo_documento=request.POST["tipo_documento"],
                                            num_documento=request.POST["num_documento"],
                                            temp_password=request.POST["password"],
                                            is_active=False)
            rol_lector = Roles.objects.get(rol='L')
            user.roles.add(rol_lector)
            user.save()
            return redirect('Usuarios')
    else:
        return render(request, 'Dashboard/register.html')
      
@login_required(login_url=('/login'))
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuarios, id=usuario_id)
    roles = list(usuario.roles.all())
    usuario.delete()
    for rol in roles:
        rol.usuarios_set.remove(usuario)
    return JsonResponse({'mensaje': 'Usuario eliminado exitosamente.'})
  
  
def act_info(request):
    return render(request, 'Dashboard/code_iv.html')


def grupos_Investigacion(request):
    if request.method == 'GET':
        # Filtra los registros que no tienen campos vacíos
        data = list(Listas_plegables.objects.exclude(
            nombre_grupo_investigacion__isnull=True,
            nombre_grupo_investigacion__exact='',
            codigos_grupo_investigacion__isnull=True,
            codigos_grupo_investigacion__exact=''
        ).values('nombre_grupo_investigacion', 'codigos_grupo_investigacion'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def redes_de_conocimiento(request):
    if request.method == 'GET':
        # Filtra los registros que no tienen campos vacíos
        data = list(Listas_plegables.objects.exclude(
            redes_conocimiento__isnull=True,
            redes_conocimiento__exact='',
        ).values('redes_conocimiento'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def subareas_de_conocimiento(request):
    if request.method == 'GET':
        data = list(Listas_plegables.objects.exclude(
            subareas_conocimiento__isnull=True,
            subareas_conocimiento__exact='',
        ).values('subareas_conocimiento'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def diciplina_de_subarea(request):
    if request.method == 'GET':
        data = list(Listas_plegables.objects.exclude(
            diciplina_subarea__isnull=True,
            diciplina_subarea__exact='',
        ).values('diciplina_subarea'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def nombre_de_centro_formacion(request):
    if request.method == 'GET':
        data = list(Listas_plegables.objects.exclude(
            nombre_centro_formacion__isnull=True,
            nombre_centro_formacion__exact='',
        ).values('nombre_centro_formacion'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)