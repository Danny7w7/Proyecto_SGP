from django.shortcuts import redirect, render
from app.forms import AutoresForm, ProyectoForm, Informacion_de_centroForm
from app.models import Proyecto


def crear_proyecto_view(request):
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('info_proyecto')
           
    else:
        form = ProyectoForm()

    context = {'form': form}
    return render(request, 'crearp.html', context)

# Informacion proponente
def Informacion_de_centro_view(request):
    if request.method == "POST":
        form = Informacion_de_centroForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Informacion_de_centroForm()
    
    context = {'form': form}
    return render(request, 'infop.html', context)

def  Autores_view(request):
    if request.method == "POST":
        form = AutoresForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AutoresForm()
    
    context = {'form': form}
    return render(request, 'infop.html', context)
