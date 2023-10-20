
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import Informacion_proponenteForm, ProyectoForm
from app.models import  Proyecto, Informacion_proponente
from django.contrib.auth.decorators import login_required
from app.views.index import index
#Listas desplegables
from app.models import Codigos_grupo_investigacion, Nombre_grupo_investigacion, Redes_conocimiento, Subareas_conocimiento, Diciplina_subarea

#------Decoradores------
def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)

#------Formulario------
@login_required(login_url='/login') 
def crear_proyecto(request):
    if user_has_role(request.user, 'Admin', 'F'):
        if request.method == 'POST':
            form = ProyectoForm(request.POST)
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.usuario = request.user
                proyecto.save()
                return redirect('info_proyecto', id_proyecto=proyecto.id)
        else:
            form = ProyectoForm()
            context = {'form': form,
                        'listaPlegable':contex_form()}
    return render(request, 'form/crearp.html', context)

def informacion_proponente(request, id_proyecto):
    context = {'proyecto':get_object_or_404(Proyecto, id=id_proyecto),
               'infoProyecto':get_object_or_404(Informacion_proponente)}
    return render(request, 'form/infop.html', context)

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


#------JSON------
def info_proponente(request, id_proyecto):
    try:
        informacion_proponente = Informacion_proponente.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        informacion_proponente = Informacion_proponente.objects.create(proyecto=proyecto)
    model = Informacion_proponente
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        setattr(informacion_proponente, name, request.POST.get(name))
    try:
        informacion_proponente.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


  
#------Editar proyecto------
def edit_proyect(request, id_proyecto):
    user = request.user
    proyecto = Proyecto.objects.filter(id=id_proyecto).first()
    if not user.id == proyecto.usuario_id:
        return redirect(index)
    if request.method == 'POST':

        model = Proyecto
        column_names = [field.name for field in model._meta.fields]
        
        for name in column_names:
            if name == 'id' or name == 'usuario':
                continue
            setattr(proyecto, name, request.POST.get(name))
        proyecto.save()

    context = {'proyecto':user.proyecto_set.first(),
            'listaPlegable':contex_form()}
    return render(request, 'edit_form/edit_proy.html', context)

