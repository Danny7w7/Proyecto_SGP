
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import Informacion_proponenteForm, ObjetivoEspecificoForm, ProyectoForm, ObjetivoForm, DocumentForm, ObjetivoEspecificoForm
from app.models import  Proyecto, Informacion_proponente, Proyecto, Objetivos, UltimaVista, Document, Objetivos_especificos
from django.contrib.auth.decorators import login_required
from app.views.index import index
#Listas desplegables
from app.models import Codigos_grupo_investigacion, Nombre_grupo_investigacion, Redes_conocimiento, Subareas_conocimiento, Diciplina_subarea

#------Decoradores------
def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)

#------Funciones generales------
def progress_bar(id):
    proyecto = Proyecto.objects.get(id=id)
    print(proyecto.progress)
    return round((proyecto.progress / 89) * 100, 1)
# Falta ponerlo a funcionar en todos los formularios y que tambien trabaje con AJAX que va a implementar Miguel.

def own_user(user, proyecto_id):
    proyecto = Proyecto.objects.filter(id=proyecto_id).first()
    return user.id == proyecto.usuario_id

#------Formulario------
@login_required(login_url='/login')
def crear_proyecto(request):
    if user_has_role(request.user, 'Admin', 'F'):
        if request.method == 'POST':
            form = ProyectoForm(request.POST)
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.usuario = request.user
                proyecto.progress = 10
                proyecto.save()
                return redirect('info_proyecto', id_proyecto=proyecto.id)
        else:
            form = ProyectoForm()
            context = {'form': form,
                       'listaPlegable':contex_form(),
                       'percentaje':0}
        return render(request, 'form/crearp.html', context)
    return redirect('index')

def informacion_proponente(request, id_proyecto):
    context = {'proyecto':get_object_or_404(Proyecto, id=id_proyecto),
               'infoProyecto':get_object_or_404(Informacion_proponente)}
    return render(request, 'form/infop.html', context)

def Informacion_de_centro(request, id_proyecto):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    if request.method == 'POST':
        form = Informacion_proponenteForm(request.POST)
        if form.is_valid():
            informacion_centro = form.save(commit=False)   
            informacion_centro.proyecto = proyecto
            informacion_centro.save()
            proyecto.progress += 9
            proyecto.save()
            print("Información del centro guardada correctamente.")
        else:
            print(form.errors)
            print("El formulario no es válido.")

    form = Informacion_proponenteForm(initial={'proyecto': proyecto})
    percentaje = progress_bar(id_proyecto)
    context = {'form':form,
                'proyecto':proyecto,
                'percentaje':percentaje}

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
    if not own_user(user, proyecto.id):
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


def guardar_objetivos(request, objetivo_proyecto_id):
    objetivo = get_object_or_404(Proyecto, id=objetivo_proyecto_id)
    
    if request.method == 'POST':
        objetivo_form = ObjetivoForm(request.POST)
        objetivo_especifico_form = ObjetivoEspecificoForm(request.POST)

        if objetivo_form.is_valid() and objetivo_especifico_form.is_valid():
            # Crear o recuperar el objetivo general
            objetivo_general, created = Objetivos.objects.get_or_create(objetivo_proyecto=objetivo)

            # Actualizar el objetivo general con la información del formulario ObjetivoForm
            objetivo_general.objetivo_general = objetivo_form.cleaned_data['objetivo_general']
            objetivo_general.save()

            # Crear el objetivo específico asociado al objetivo general usando ObjetivoEspecificoForm
            Objetivos_especificos.objects.create(objetivo_especificos=objetivo_especifico_form.cleaned_data['objetivo_especificos'], objetivos=objetivo_general)

            print("Los objetivos se guardaron correctamente.")
        else:
            print("Uno o ambos formularios no son válidos.")
    else:
        objetivo_form = ObjetivoForm()
        objetivo_especifico_form = ObjetivoEspecificoForm()

    return render(request, 'form/objetivos.html', {'objetivo_form': objetivo_form, 'objetivo_especifico_form': objetivo_especifico_form, 'objetivo': objetivo})

def editar_objetivo(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)

    objetivo_general, created = Objetivos.objects.get_or_create(objetivo_proyecto=proyecto)
    objetivo_especifico = objetivo_general.objetivosespecificos_set.first()

    if request.method == 'POST':
        form = ObjetivoEspecificoForm(request.POST, instance=objetivo_especifico)
        if form.is_valid():
            objetivo_especifico = form.save(commit=False)
            objetivo_especifico.objetivos = objetivo_general
            objetivo_especifico.save()
            print("El objetivo específico se actualizó correctamente.")
            return redirect('index')
    else:
        form = ObjetivoEspecificoForm(instance=objetivo_especifico)

    return render(request, 'edit_form/edit_objet.html', {'form': form, 'proyecto': proyecto, 'objetivo_general': objetivo_general, 'objetivo_especifico': objetivo_especifico})


def proyectos_usuario(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    if request:
        return render(request, 'proyectos.html', {'proyectos': proyectos})
    else:
         return redirect('continuar_sesion')


def continuar_sesion(request):
    if request.user.is_authenticated:
        ultima_vista = UltimaVista.objects.filter(usuario=request.user).first()
        if ultima_vista:
            return redirect(ultima_vista.ultima_vista)
    return redirect(proyectos_usuario)


def subir_anexos(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            anexo = form.save(commit=False)
            anexo.proyecto = proyecto
            anexo.save()
    
    documents = Document.objects.filter(proyecto=proyecto)
    return render(request, "form/anexos.html", {"docs": documents, "proyecto": proyecto})


def editar_anexo(request, proyecto_id):
    try:
        proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
        anexo = Document.objects.filter(proyecto=proyecto).first()
        print(anexo)
    except:
        return redirect('subir_anexos', proyecto_id)

    if request.method == "POST":
        model = Document
        column_names = [field.name for field in model._meta.fields]
        
        for name in column_names:
            if name == 'id' or name == 'fecha' or name == 'proyecto_id' or request.FILES.get(name) == None:
                continue
            setattr(anexo, name, request.FILES.get(name))
        anexo.save()

    form = DocumentForm()
    return render(request, "edit_form/edit_anexos.html", {"form": form, "proyecto": proyecto})

    

