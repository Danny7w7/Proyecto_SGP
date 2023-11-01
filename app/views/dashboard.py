#Funciones de ADMIN MENU
from django.http import HttpResponse
from django.shortcuts import redirect, render
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

# def editar_permisos(request, usuario_id):
#     if request.method == 'POST':
#         nuevos_roles = request.POST.getlist('roles')
#         usuario = Usuarios.objects.get(id=usuario_id)
#         usuario.roles.set(Roles.objects.filter(rol__in=nuevos_roles))

#     return redirect('usuarios')

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