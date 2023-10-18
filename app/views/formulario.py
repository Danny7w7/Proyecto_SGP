
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import Informacion_proponenteForm, ProyectoForm
from app.models import  Codigos_grupo_investigacion, Nombre_grupo_investigacion, Redes_conocimiento, Subareas_conocimiento, Diciplina_subarea, Proyecto
from django.contrib.auth.decorators import login_required


def edit_proyect(request):
    user = request.user
    proyecto = user.proyecto_set.first()
    print(proyecto)
    if request.method == 'POST':
        #Aqui se va a obtener el proyecto asociado al usuario (Cuando Cova termine la asociacion :v)

        model = Proyecto
        column_names = [field.name for field in model._meta.fields]
        
        for name in column_names:
            if name == 'id' or name == 'usuario':
                continue
            print(request.POST.get(name))
            print("Guardo"+name+"\n")
            setattr(proyecto, name, request.POST.get(name))
        proyecto.save()

    context = {'proyecto':user.proyecto_set.first(),
            'listaPlegable':contex_form()}
    return render(request, 'edit_form/edit_proy.html', context)

def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)

@login_required(login_url='/login') 
def crear_proyecto(request):
    if user_has_role(request.user, 'Admin', 'F'):
        if request.method == 'POST':
            form = ProyectoForm(request.POST)
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.usuario = request.user
                proyecto.save()
                return redirect('crear_proyecto')
        else:
            form = ProyectoForm()
    return render(request, 'form/crearp.html', {'form': form})

def Informacion_de_centro(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    if request.method == 'POST':
        form = Informacion_proponenteForm(request.POST)
        if form.is_valid():
            informacion_centro = form.save(commit=False)   
            informacion_centro.proyecto = proyecto
            informacion_centro.save()
            print("Información del centro guardada correctamente.")
        else:
            print(form.errors)
            print("El formulario no es válido.")
    else:
        form = Informacion_proponenteForm(initial={'proyecto': proyecto})
        
    return render(request, 'form/infop.html', {'form': form, 'proyecto': proyecto})

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

  
