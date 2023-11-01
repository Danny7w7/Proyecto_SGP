#Funciones de ADMIN MENU
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app.models import Usuarios, Roles


def admin(request):
    return render(request, 'Dashboard/Admin.html')

def not404(request):
    return render(request, 'Dashboard/404.html')

def anexosdoc(request):
    return render(request, 'Dashboard/Anexos.html')

def usuarios(request):
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

def preguntas(request):
    return render(request, 'Dashboard/PreguntasP.html')

def proyectosINA(request):
    return render(request, 'Dashboard/Proyectos-eliminados.html')

def proyectoP(request):
    return render(request, 'Dashboard/Proyectos-pendientes.html')

def proyectoT(request):
    return render(request, 'Dashboard/Proyectos-terminado.html')