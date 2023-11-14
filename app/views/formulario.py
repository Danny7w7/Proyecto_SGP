
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse

from app.forms import CausaForm, EfectoForm, Informacion_proponenteForm, ObjetivoEspecificoForm, ProyectoForm, ObjetivoForm, DocumentForm, ProducEsperados
from app.models import Entidades_aliadas, Causa, Efecto, Proyecto, Informacion_proponente, Generalidades_del_proyecto,Participantes_Proyecto, Autores, Resumen_antecedentes, Objetivos, Descripcion_problema, UltimaVista, Document, RiesgoObjetivoGeneral, RiesgoProductos, RiesgoActividades, Objetivos_especificos, Centro_de_formacion, Proyeccion


from django.contrib.auth.decorators import login_required
from app.views.index import index
#Listas desplegables
from app.models import Listas_plegables

import datetime
import os

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
    
def contex_form():
    lista = Listas_plegables.objects.all()
    codigos = lista.order_by('codigos_grupo_investigacion').values_list('codigos_grupo_investigacion', flat=True)
    nombres = lista.order_by('nombre_grupo_investigacion').values_list('nombre_grupo_investigacion', flat=True)
    redes = lista.order_by('redes_conocimiento').values_list('redes_conocimiento', flat=True)
    subareas = lista.order_by('subareas_conocimiento').values_list('subareas_conocimiento', flat=True)
    diciplinas = lista.order_by('diciplina_subarea').values_list('diciplina_subarea', flat=True)
    nombresC = lista.order_by('nombre_centro_formacion').values_list('nombre_centro_formacion', flat=True)
    return {'codigos':codigos,
            'nombres':nombres,
            'redes':redes,
            'subareas':subareas,
            'diciplinas':diciplinas,
            'nombresC':nombresC}

#------Formulario------
@login_required(login_url='/login')
def crear_proyecto(request):
    if not user_has_role(request.user, 'Admin', 'F'):
        return redirect('index')
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

def informacion_proponente(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
               'infoProyecto':Informacion_proponente.objects.filter(proyecto_id=get_or_none(Proyecto, id=id_proyecto)).first(),
               'autores': Autores.objects.filter(proyecto = proyecto),
               'participantes': Participantes_Proyecto.objects.filter(proyecto = proyecto),
               'percentaje':id_proyecto,
               'listaPlegable':contex_form()}
    return render(request, 'form/infop.html', context)
    

def estructura_proyecto(request, id_proyecto):
    context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
               'resumen':get_or_none(Resumen_antecedentes),
               'percentaje':id_proyecto}
    return render(request, 'form/estp.html', context)


def crear_objetivo(request, objetivo_proyecto_id):
    if request.method == 'POST':
        objetivo_proyecto_id = request.POST.get('objetivo_proyecto_id')
        proyecto = Proyecto.objects.get(id=objetivo_proyecto_id)

        objetivo_form = ObjetivoForm(request.POST)
        objetivo_especifico_form = ObjetivoEspecificoForm(request.POST)
        causa_form = CausaForm(request.POST)
        efecto_form = EfectoForm(request.POST)

        if (
            objetivo_form.is_valid() and
            objetivo_especifico_form.is_valid() and
            causa_form.is_valid() and
            efecto_form.is_valid()
        ):
            objetivo = objetivo_form.save(commit=False)
            objetivo.proyecto = proyecto
            objetivo.save()

            objetivo_especifico = objetivo_especifico_form.save(commit=False)
            objetivo_especifico.objetivos = objetivo
            objetivo_especifico.save()

            causa = causa_form.save(commit=False)
            causa.obejetivo_especifico = objetivo_especifico
            causa.save()
            
            efecto = efecto_form.save(commit=False)
            efecto.causas = causa
            efecto.save()

            objetivo_especificos2 = request.POST.get('objetivo_especificos2', '')
            causa2 = request.POST.get('causa2', '')
            efecto2 = request.POST.get('efecto2', '')

            objetivo_especificos3 = request.POST.get('objetivo_especificos3', '')
            causa3 = request.POST.get('causa3', '')
            efecto3 = request.POST.get('efecto3', '')

            if objetivo_especificos2 and causa2 and efecto2:
                objetivo_especifico2 = Objetivos_especificos.objects.create(
                    objetivos=objetivo,
                    objetivo_especificos=objetivo_especificos2,
                )
                causa2 = Causa.objects.create(
                    obejetivo_especifico=objetivo_especifico2,
                    causa=causa2,
                )
                efecto2 = Efecto.objects.create(
                    causas=causa2,
                    efecto=efecto2,
                )

            if objetivo_especificos3 and causa3 and efecto3:
                objetivo_especifico3 = Objetivos_especificos.objects.create(
                    objetivos=objetivo,
                    objetivo_especificos=objetivo_especificos3,
                )
                causa3 = Causa.objects.create(
                    obejetivo_especifico=objetivo_especifico3,
                    causa=causa3,
                )
                efecto3 = Efecto.objects.create(
                    causas=causa3,
                    efecto=efecto3,
                    )
        return redirect('participantes', objetivo_proyecto_id)
    else:
        objetivo_form = ObjetivoForm()
        objetivo_especifico_form = ObjetivoEspecificoForm()
        causa_form = CausaForm()
        efecto_form = EfectoForm()

    contex = {
        'objetivo_form': objetivo_form,
        'objetivo_especifico_form': objetivo_especifico_form,
        'causa_form': causa_form,
        'efecto_form': efecto_form,
        'proyecto': objetivo_proyecto_id,
        'percentaje': 1
    }
    return render(request, 'form/objetivos.html', contex)


def participantes(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    print(Entidades_aliadas.objects.filter(proyecto = proyecto))
    context = {
        'proyecto':get_or_none(Proyecto, id=id_proyecto),
        'entidad_a':Entidades_aliadas.objects.filter(proyecto = proyecto),
        'centro_f':Centro_de_formacion.objects.filter(proyecto = proyecto),
        'percentaje': id_proyecto
    }
    return render(request, 'form/partp.html', context)


def selectObj(request, id_proyecto):
    try:
        objGeneral = Objetivos.objects.get(proyecto=id_proyecto)
        objEspecificos = Objetivos_especificos.objects.filter(objetivos_id=objGeneral)
    except:
        return HttpResponse("Para acceder a esta vista debes de crear los objetivos especificos")
    contex = {'percentaje':1,
              'objetivosEsp':objEspecificos,
              'id_proyecto':id_proyecto}
    return render(request, 'form/selectObj.html', contex)


def producEsperados(request, id_proyecto, id_objetivoEsp):
    objGeneral = Objetivos.objects.get(proyecto=id_proyecto)
    objEspecifico = Objetivos_especificos.objects.get(objetivos_id=objGeneral, id=id_objetivoEsp)
    if request.method == 'POST':
        form = ProducEsperados(request.POST)
        if form.is_valid():
            produc = form.save(commit=False)
            produc.objetivo_especifico_id = objEspecifico.id
            produc.save()
            return redirect('seleccionarObjetivo', id_proyecto)
    form = ProyectoForm()
    contex = {'percentaje':1,
              'objEspecifico':objEspecifico}
    return render(request, 'form/producEsperados.html', contex)


def proyeccion(request, id_proyecto):
    contex = {'percentaje':1,
              'proyecto':get_or_none(Proyecto, id=id_proyecto)}
    return render(request, 'form/proyeccion.html', contex)
  
  
def riesgo_general(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    
    riesgos_g = get_or_none(RiesgoObjetivoGeneral, proyecto=id_proyecto)
    riesgos_p = get_or_none(RiesgoProductos, proyecto=id_proyecto)
    riesgos_a = get_or_none(RiesgoActividades, proyecto=id_proyecto)
    
    context = {
        'proyecto': proyecto,
        'riesgos_g': riesgos_g,
        'riesgos_p': riesgos_p,
        'riesgos_a': riesgos_a,
        'percentaje': 1
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


def subir_anexos(request, proyecto_id):
    proyecto = get_or_none(Proyecto, pk=proyecto_id)
    
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            anexo = form.save(commit=False)
            anexo.proyecto = proyecto
            anexo.save()
    documents = Document.objects.filter(proyecto=proyecto)
    contex = {'docs':documents,
              'proyecto':proyecto,
            'percentaje':proyecto_id}
    return render(request, "form/anexos.html", contex)



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
    
def info_autores(request, id_proyecto):


    proyecto = Proyecto.objects.get(id=id_proyecto)
    autores = Autores(proyecto=proyecto)  # Crea una nueva instancia en lugar de obtener una existente

    model = Autores
    column_names = [field.name for field in model._meta.fields]
    
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(autores, name, request.POST.get(name))
    try:
        autores.save()
        return JsonResponse({"mensaje": "Operación exitosa", "nuevo_autor": {
            "nombre_Autor_Proyecto": autores.nombre_Autor_Proyecto,
            "tipo_Vinculacion_entidad": autores.tipo_Vinculacion_entidad,
            "numero_Cedula_Autor": autores.numero_Cedula_Autor,
            "rol_Sennova_De_Participantes_de_Proyecto": autores.rol_Sennova_De_Participantes_de_Proyecto,
            "email_Autor_Proyecto": autores.email_Autor_Proyecto,
            "numero_Telefono_Autor": autores.numero_Telefono_Autor
        }})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_participantes(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    participante = Participantes_Proyecto(proyecto=proyecto)
        
    model = Participantes_Proyecto
    column_names = [field.name for field in model._meta.fields]
        
    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(participante, name, request.POST.get(name))
    try:
        participante.save()
        return JsonResponse({"mensaje": "Operación exitosa", "nuevo_participante": {
            "nombre_participantes_de_desarrollo":participante.nombre_participantes_de_desarrollo,
            "numero_cedula_participantes": participante.numero_cedula_participantes,
            "numero_meses_vinculacion_participantes": participante.numero_meses_vinculacion_participantes,
            "email_participantes_de_desarrollo": participante.email_participantes_de_desarrollo,
            "numero_horas_Semanales_dedicadas_participantes": participante.numero_horas_Semanales_dedicadas_participantes,
            "numero_Telefono_participantes": participante.numero_Telefono_participantes
        }})
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


def resumen_antecedentes(request, id_proyecto):
    try:
        resumen = Resumen_antecedentes.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        resumen = Resumen_antecedentes.objects.create(proyecto=proyecto)
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
    descripcion.identificacion_y_descripcion_problema = request.POST['Identificacion_y_descripcion_problema']
    descripcion.justificacion = request.POST['Justificacion']
    try:
        os.remove('media/' + descripcion.marco_conceptual.name)
    except:
        print("No existe la foto o es primera vez")
    descripcion.marco_conceptual = request.FILES['Marco_conceptual'] 
    
    try:
        descripcion.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def entidad_aliada(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    centro = Entidades_aliadas(proyecto=proyecto)
   
    model = Entidades_aliadas
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(centro, name, request.POST.get(name))
    try:
            centro.save()
            return JsonResponse({"mensaje": "Operación exitosa", "nueva_entidad": {
                "nombre_entidad":centro.nombre_entidad,
                "tipo_entidad_aliada": centro.tipo_entidad_aliada,
                "naturaleza_entidad": centro.naturaleza_entidad,
                "clasificacion_empresa": centro.clasificacion_empresa,
                "nit": centro.nit
            }})
    except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def centro_formacion(request, id_proyecto):
    try:
        centro_f = Centro_de_formacion.objects.get(proyecto_id=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        centro_f = Centro_de_formacion.objects.create(proyecto=proyecto)
   
    model = Centro_de_formacion
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == 'id' or name == 'proyecto':
            continue
        
        setattr(centro_f, name, request.POST.get(name))

    try:
        centro_f.save()
        # print("Guardado exitosamente")
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def tiempo_ejecucion(request, id_proyecto):
    try:
        tiempo = Proyeccion.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        tiempo = Proyeccion.objects.create(proyecto=proyecto)
    tiempo.duracion = request.POST['duracion']
    tiempo.fch_inicio = request.POST['fch_inicio']
    tiempo.fch_cierre = request.POST['fch_cierre']
    try:
        tiempo.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def cadena_valor(request, id_proyecto):
    try:
        cadena = Proyeccion.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        cadena = Proyeccion.objects.create(proyecto=proyecto)
    cadena.cadena_valor = request.FILES['Cadena_valor']
    cadena.propuesta_sostenibilidad = request.POST['Propuesta_sostenibilidad']
    cadena.impacto_social = request.POST['Impacto_social']
    cadena.impacto_tecnologico = request.POST['Impacto_tecnologico']
    cadena.impacto_centro_formacion = request.POST['Impacto_centro']
    try:
        cadena.save()
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
               'listaPlegable':contex_form(),
               'percentaje':id_proyecto}
    return render(request, 'edit_form/edit_proy.html', context)


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
    return render(request, "edit_form/edit_anexos.html", {"form": form, "proyecto": proyecto, "percentaje" : 0})


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

