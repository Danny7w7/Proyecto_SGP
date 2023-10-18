#Funciones de ADMIN MENU
from django.shortcuts import render


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