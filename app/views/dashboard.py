#Funciones de ADMIN MENU
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.models import Usuarios, Roles
from django.contrib.auth.decorators import login_required


def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)


@login_required(login_url='/login')
def admin(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Admin.html')

def not404(request):
    return render(request, 'Dashboard/404.html')

@login_required(login_url='/login')
def anexosdoc(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Anexos.html')


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