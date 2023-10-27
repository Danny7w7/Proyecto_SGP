
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.forms import Informacion_proponenteForm, ProyectoForm, ObjetivoForm, DocumentForm
from app.models import  Proyecto, Informacion_proponente, Generalidades_del_proyecto,Participantes_Proyecto, Autores, Resumen_antecedentes, Objetivos, Descripcion_problema, UltimaVista, Document, RiesgoObjetivoGeneral, RiesgoProductos, RiesgoActividades

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

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

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
    context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
               'infoProyecto':Informacion_proponente.objects.filter(proyecto_id=get_or_none(Proyecto, id=id_proyecto)).first()}
    return render(request, 'form/infop.html', context)

def estructura_proyecto(request, id_proyecto):
    context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
               'resumen':get_or_none(Resumen_antecedentes)}
    return render(request, 'form/estp.html', context)








# def riesgo_general(request, id_proyecto):
#     context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
#                'riesgos_g':get_or_none(RiesgoObjetivoGeneral, proyecto=id_proyecto)}
#     cnt = get_or_none(RiesgoObjetivoGeneral, proyecto=id_proyecto)
#     return render(request, 'form/riesgosp.html', context)

# def riesgo_producto(request, id_proyecto):
#     context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
#                'riesgos_p':get_or_none(RiesgoProductos, proyecto= id_proyecto)}
#     cnt2 = get_or_none(RiesgoProductos, proyecto=id_proyecto)
#     return render(request, 'form/riesgosp.html', context)

# def riesgo_actividad(request, id_proyecto):
#     context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
#                'riesgos_a':get_or_none(RiesgoActividades, proyecto=id_proyecto)}
#     cnt3= get_or_none(RiesgoActividades, proyecto=id_proyecto)
#     return render(request, 'form/riesgosp.html', context)
def riesgo_general(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    
    riesgos_g = get_or_none(RiesgoObjetivoGeneral, proyecto=id_proyecto)
    riesgos_p = get_or_none(RiesgoProductos, proyecto=id_proyecto)
    riesgos_a = get_or_none(RiesgoActividades, proyecto=id_proyecto)
    
    context = {
        'proyecto': proyecto,
        'riesgos_g': riesgos_g,
        'riesgos_p': riesgos_p,
        'riesgos_a': riesgos_a
    }
    
    return render(request, 'form/riesgosp.html', context)


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

def resumen_antecedentes(request, id_proyecto):
    try:
        resumen = Resumen_antecedentes.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        resumen = Resumen_antecedentes.objects.create(proyecto=proyecto)
    print('Prueba esta mierda mamaguevo')
    resumen.resumen_ejecutivo = request.POST['Resumen_ejecutivo']
    resumen.antecedentes = request.POST['Antecedentes']
    try:
        resumen.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def descripcion_problema(request, id_proyecto):
    try:
        descripcion = Descripcion_problema.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        descripcion = Descripcion_problema.objects.create(proyecto=proyecto)
    print('Prueba esta mierda mamaguevo')
    descripcion.identificacion_y_descripcion_problema = request.POST['Identificacion_y_descripcion_problema']
    descripcion.justificacion = request.POST['Justificacion']
    descripcion.marco_conceptual = request.FILES['Marco_conceptual']
    try:
        descripcion.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def info_autores(request, id_proyecto):
    try:
        autores = Autores.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        autores = Autores.objects.create(proyecto=proyecto)
       
    model = Autores
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(autores, name, request.POST.get(name))
    try:
        autores.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_participantes(request, id_proyecto):
    try:
        participantes = Participantes_Proyecto.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        participantes = Participantes_Proyecto.objects.create(proyecto=proyecto)
       
    model = Participantes_Proyecto
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(participantes, name, request.POST.get(name))
    try:
        participantes.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_generalidades(request, id_proyecto):
    try:
        generalidades = Generalidades_del_proyecto.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        generalidades = Generalidades_del_proyecto.objects.create(proyecto=proyecto)
       
    model = Generalidades_del_proyecto
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(generalidades, name, request.POST.get(name))
    try:
        generalidades.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    






def riesgos_obj_g_json(request, id_proyecto):
    try:
        riesgos_obj_g_json = RiesgoObjetivoGeneral.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        riesgos_obj_g_json = RiesgoObjetivoGeneral.objects.create(proyecto=proyecto)
    model = RiesgoObjetivoGeneral
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        setattr(riesgos_obj_g_json, name, request.POST.get(name))
    try:
        riesgos_obj_g_json.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def riesgos_p_json(request, id_proyecto):
    try:
        riesgos_p_json = RiesgoProductos.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        riesgos_p_json = RiesgoProductos.objects.create(proyecto=proyecto)
    model = RiesgoProductos
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        setattr(riesgos_p_json, name, request.POST.get(name))
    try:
        riesgos_p_json.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def riesgo_a_json(request, id_proyecto):
    try:
        riesgo_a_json = RiesgoActividades.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        riesgo_a_json = RiesgoActividades.objects.create(proyecto=proyecto)
    model = RiesgoActividades
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        setattr(riesgo_a_json, name, request.POST.get(name))
    try:
        riesgo_a_json.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# ---FIN YEISON ---
  
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

