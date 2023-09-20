from django.shortcuts import redirect, render
from app.forms import AutoresForm, ProyectoForm, Informacion_de_centroForm, ParticipantesForm, Informacion_ProyectoForm, Estructura_del_proyectoForm, Analisis_ParticipantesForm, Entidades_aliadasForm
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

def  Participantes_view(request):
    if request.method == "POST":
        form = ParticipantesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ParticipantesForm()
    
    context = {'form': form}
    return render(request, 'infop.html', context)

def  Informacion_Proyecto_view(request):
    if request.method == "POST":
        form = Informacion_ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Informacion_ProyectoForm()
    
    context = {'form': form}
    return render(request, 'infop.html', context)

def  Estructura_del_proyecto_view(request):
    if request.method == "POST":
        form = Estructura_del_proyectoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Estructura_del_proyectoForm()
    
    context = {'form': form}
    return render(request, 'estp.html', context)

def  Analisis_Participantes_view(request):
    if request.method == "POST":
        form = Analisis_ParticipantesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Analisis_ParticipantesForm()
    
    context = {'form': form}
    return render(request, 'partp.html', context)

def  Entidades_aliadas_view(request):
    if request.method == "POST":
        form = Entidades_aliadasForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Entidades_aliadasForm()
    
    context = {'form': form}
    return render(request, 'partp.html', context)
