from django.shortcuts import redirect, render
from app.forms import AutoresForm, ParticipantesForm, ProyectoForm, Informacion_de_centroForm, Informacion_ProyectoForm, Estructura_del_proyectoForm, Analisis_ParticipantesForm, Entidades_aliadasForm, RiesgoObjetivoGeneralForm, RiesgoProductosForm, RiesgoActividadesForm, Estructura_arbol_problemasForm, Estructura_problemaForm
from app.models import Autores, Participantes_Proyecto, Proyecto
from django.http import JsonResponse


def index_view(request):
    
    return render(request, 'index.html')

def crear_proyecto_view(request):
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('info_proyecto')
        
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

# Mostrar info de autores
def Mostrar_autores(request):
    m_autores = Autores.objects.all()  # obtiene todos los registros del modelo
    return render(request, 'infop.html', {'m_autores': m_autores})

def  Participantes_view(request):
    if request.method == "POST":
        form = ParticipantesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ParticipantesForm()
    
    context = {'form': form}
    return render(request, 'infop.html', context)


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
    
def  Estructura_arbol_problemas_view(request):
    if request.method == "POST":
        form = Estructura_arbol_problemasForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Estructura_arbol_problemasForm()
    
    context = {'form': form}
    return render(request, 'estp.html', context)

def  Estructura_problema_view(request):
    if request.method == "POST":
        form = Estructura_problemaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Estructura_problemaForm()
    
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

def Riesgos_objetivo_general_view(request):
    if request.method == 'POST':
        form = RiesgoObjetivoGeneralForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RiesgoObjetivoGeneralForm()

    context = {'form': form}
    return render(request, 'riesgosp.html', context)

def Riesgo_productos_view(request):
    if request.method == 'POST':
        form = RiesgoProductosForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RiesgoProductosForm()

    context = {'form': form}
    return render(request, 'riesgosp.html', context)

def Riesgo_actividades_view(request):
    if request.method == 'POST':
        form = RiesgoActividadesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RiesgoActividadesForm()

    context = {'form': form}
    return render(request, 'riesgosp.html', context)
