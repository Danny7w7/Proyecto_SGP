
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import Informacion_proponenteForm, ProyectoForm , ObjetivoForm , DocumentForm
from app.models import  Codigos_grupo_investigacion, Nombre_grupo_investigacion, Redes_conocimiento, Subareas_conocimiento, Diciplina_subarea, Proyecto, Objetivos , UltimaVista , Document
from django.contrib.auth.decorators import login_required
from app.views.index import index

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
        form = ObjetivoForm(request.POST)
        if form.is_valid():
            objetivo_nuevo = form.save(commit=False)
            objetivo_nuevo.objetivo_proyecto = objetivo
            objetivo_nuevo.save()
            print("Los objetivos se guardaron correctamente.")
        else:
            print(form.errors)
            print("El formulario no es válido.")
    else:
        form = ObjetivoForm(initial={'objetivo': objetivo})
        
    return render(request, 'form/objetivos.html', {'form': form, 'objetivo': objetivo})


def editar_objetivo(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    
    objetivo_general = Objetivos.objects.filter(objetivo_proyecto=proyecto).first()

    if request.method == 'POST':
        form = ObjetivoForm(request.POST, instance=objetivo_general)
        if form.is_valid():
            objetivo_general = form.save(commit=False)
            objetivo_general.objetivo_proyecto = proyecto
            objetivo_general.save()
            print("El objetivo se actualizó correctamente.")
            return redirect('index')
    else:
        form = ObjetivoForm(instance=objetivo_general)

    return render(request, 'edit_form/edit_objet.html', {'form': form, 'proyecto': proyecto, 'objetivo_general': objetivo_general})

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
        for i in range(1, 7):
            nombre_anexo = f'anexo{i}'
            archivo = request.FILES.get(nombre_anexo, None)
            if archivo:
                # Crear un nuevo objeto Document asociado al proyecto
                document = Document(proyecto=proyecto)
                setattr(document, nombre_anexo, archivo)
                document.save()

    documents = Document.objects.filter(proyecto=proyecto)
    return render(request, "form/anexos.html", context={"docs": documents, "proyecto": proyecto})


def editar_anexo(request, proyecto_id, documento_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    document = get_object_or_404(Document, pk=documento_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('subir_anexos', proyecto_id=proyecto_id)
        else:
            print(form.errors)
    else:
        form = DocumentForm(instance=document)

    return render(request, "edit_form/edit_anexos.html", context={"form": form, "proyecto": proyecto, "document": document})