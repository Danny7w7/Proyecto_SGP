import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.core.serializers import serialize
from django.conf import settings
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Frame, PageTemplate
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.forms import (
    Informacion_proponenteForm,
    ProyectoForm,
    ProducEsperadosForm,
)

from app.models import (
    Anexos,
    Centro_formacion,
    Entidades_aliadas,
    Estado,
    Proyecto,
    Informacion_proponente,
    Generalidades_del_proyecto,
    Participantes_Proyecto,
    Autores,
    Region,
    Regional,
    Resultados_y_productos_esperados,
    Resumen_antecedentes,
    Objetivos,
    Descripcion_problema,
    UltimaVista,
    Document,
    RiesgoObjetivoGeneral,
    RiesgoProductos,
    RiesgoActividades,
    Objetivos_especificos,
    Centro_de_formacion,
    Proyeccion,
    Participantes_entidad_alidad,
    CronogramaAct,
    Presupuesto,
    Rubro,
    TipoRubro,
    PreguntasP,
    Respuestas
)


from django.contrib.auth.decorators import login_required
from app.views.index import index

# Listas desplegables
from app.models import Listas_plegables

from datetime import datetime
import json

# PDF
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from app.utils import mostrar_error


# ------Decoradores------
def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list("rol", flat=True))
    required_roles = set(roles)

    return bool(user_roles & required_roles)


# ------Funciones generales------

def deleteSpacesInText(spaces):
    text = re.sub(r'[\r\n]+', ' ', spaces)
    return text

def progress_bar(id):
    proyecto = Proyecto.objects.get(id=id)
    print(proyecto.progress)
    return round((proyecto.progress / 89) * 100, 1)


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
    codigos = lista.values_list(
        "codigos_grupo_investigacion", flat=True
    )
    nombres = lista.values_list(
        "nombre_grupo_investigacion", flat=True
    )
    redes = lista.order_by("redes_conocimiento").values_list(
        "redes_conocimiento", flat=True
    )
    subareas = lista.order_by("subareas_conocimiento").values_list(
        "subareas_conocimiento", flat=True
    )
    diciplinas = lista.order_by("diciplina_subarea").values_list(
        "diciplina_subarea", flat=True
    )
    nombresC = lista.order_by("nombre_centro_formacion").values_list(
        "nombre_centro_formacion", flat=True
    )
    actividades = lista.order_by("actividades_economicas").values_list(
        "actividades_economicas", flat=True
    )
    return {
        "codigos": codigos,
        "nombres": nombres,
        "redes": redes,
        "subareas": subareas,
        "diciplinas": diciplinas,
        "nombresC": nombresC,
        "actividades": actividades
    }

def generar_c_valor(request, proyecto_id):
    # Obtener el proyecto y otros datos relacionados
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    objetivos = Objetivos.objects.filter(proyecto=proyecto).first()
    objetivos_especificos = Objetivos_especificos.objects.filter(objetivoGeneral=objetivos)

    
    # Renderizar el template con los datos
    context = {
        "proyecto": proyecto,
        'objetivos': objetivos,
        "objetivos_especificos": objetivos_especificos,
    }

    template_path = "form/cadena_valor.html"
    html = render_to_string(template_path, context)

    # Lógica para generar el informe PDF a partir del HTML con xhtml2pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=cadena_valor.pdf"

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return mostrar_error(request,"Error al generar el PDF", status=500)

    return response



# ------Formulario------
@login_required(login_url="/login")
def crear_proyecto(request):
    if not user_has_role(request.user, "Admin", "F"):
        return redirect("index")
    if request.method == "POST":
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            print(request.POST.get('titulo_Proyecto'))
            proyecto.titulo_Proyecto = deleteSpacesInText(request.POST.get('titulo_Proyecto'))
            proyecto.descripcion = deleteSpacesInText(request.POST.get('descripcion'))
            proyecto.usuario = request.user
            proyecto.progress = 10
            proyecto.save()
            estado = Estado(proyecto_id=proyecto.id)
            estado.state = 2
            estado.save()
            return redirect("info_proyecto", id_proyecto=proyecto.id)
    else:
        form = ProyectoForm()

    context = {"form": form, "listaPlegable": contex_form(), "percentaje": 0}
    return render(request, "form/crearp.html", context)


@login_required(login_url="/login")
def informacion_proponente(request, id_proyecto):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    context = {'proyecto':get_or_none(Proyecto, id=id_proyecto),
               'anexo' : Anexos.objects.filter(proyecto_id=get_or_none(Proyecto, id=id_proyecto)),
               'infoProyecto':Informacion_proponente.objects.filter(proyecto_id=get_or_none(Proyecto, id=id_proyecto)).first(),
               'autores': Autores.objects.filter(proyecto = proyecto),
               'participantes': Participantes_Proyecto.objects.filter(proyecto = proyecto),
               'generalidades':get_or_none(Generalidades_del_proyecto, proyecto=id_proyecto),
               'percentaje':id_proyecto,
               'preguntas':PreguntasP.objects.all(),
               'respuestas':Respuestas.objects.filter(generalidad_id=get_or_none(Generalidades_del_proyecto, proyecto=id_proyecto)),  # Obtener las respuestas asociadas a las generalidades del proyecto
               'listaPlegable':contex_form()}
    return render(request, 'form/infop.html', context)


@login_required(login_url="/login")
def estructura_proyecto(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    if not own_user(request.user, proyecto.id):
        return redirect(index)
    context = {'proyecto':proyecto,
               'resumen':get_or_none(Resumen_antecedentes, proyecto=proyecto),
               'problema':get_or_none(Descripcion_problema, proyecto=id_proyecto),
               'percentaje':id_proyecto}
    return render(request, 'form/estp.html', context)


@login_required(login_url='/login')
def objetivo(request, id_proyecto):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    objetivo = get_or_none(Objetivos, proyecto=id_proyecto)
    try:
        objEspe = Objetivos_especificos.objects.filter(objetivoGeneral=objetivo.id)
    except:
        objEspe = None
    contex = {'percentaje':id_proyecto,
              'id_proyecto':id_proyecto,
              'objetivo':objetivo,
              'objEsp':objEspe}
    return render(request, 'form/objetivos.html', contex)


@login_required(login_url="/login")
def participantes(request, id_proyecto):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    try:
        objGeneral = Objetivos.objects.get(proyecto=proyecto.id)
    except Objetivos.DoesNotExist:
        return mostrar_error(request, 'Para acceder a esta vista por favor cree un Objetivo general del proyecto')
    context = {
        "proyecto": proyecto,
        "entidad_a": Entidades_aliadas.objects.filter(proyecto=proyecto),
        "centro_f": Centro_de_formacion.objects.filter(proyecto=proyecto).first(),
        "objEspecificos": Objetivos_especificos.objects.filter(objetivoGeneral=objGeneral),
        "listaPlegable": contex_form(),
        "percentaje": id_proyecto,
    }
    return render(request, "form/partp.html", context)

#Fech para obtener los objetivos especificos 
@csrf_exempt
def getObjEspecificos(request, id_entidad):
    entidad_aliada = Entidades_aliadas.objects.get(id=id_entidad)
    objetivos_especificos_asociados = entidad_aliada.objetivo_especificos.all()
    # Convertir los datos del queryset a una estructura serializable
    objetivos_serializados = list(objetivos_especificos_asociados.values())
    
    return JsonResponse({
        "mensaje": "Operación exitosa", 
        "id_objetivos_asociados": {
            "id": objetivos_serializados
        }
    })


@login_required(login_url="/login")
def selecEntidad(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    if not own_user(request.user, proyecto.id):
        return redirect(index)
    if not Entidades_aliadas.objects.filter(proyecto=proyecto).exists():
        return mostrar_error(request,"Para acceder a esta vista debes de crear por lo menos una entidad aliada")
    contex = {
        "entidades": Entidades_aliadas.objects.filter(proyecto=proyecto),
        "percentaje": proyecto.id,
    }
    return render(request, "form/selectEntidad.html", contex)


@login_required(login_url="/login")
def parcipantes_entidad(request, id_proyecto, id_entidad):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    entidad = Entidades_aliadas.objects.get(id=id_entidad)
    contex = {
        "percentaje": id_proyecto,
        "entidad_id": id_entidad,
        "participantes": Participantes_entidad_alidad.objects.filter(
            entidad=entidad.id
        ),
    }
    return render(request, "form/part_Entidad.html", contex)


@login_required(login_url="/login")
def selectObj(request, id_proyecto):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    try:
        objGeneral = Objetivos.objects.get(proyecto=id_proyecto)
        objEspecificos = Objetivos_especificos.objects.filter(objetivoGeneral=objGeneral)
    except:
        return mostrar_error(request,
            "Para acceder a esta vista debes de crear los objetivos especificos"
        )
    contex = {
        "percentaje": id_proyecto,
        "objetivosEsp": objEspecificos,
        "id_proyecto": id_proyecto,
    }
    return render(request, "form/selectObj.html", contex)


@login_required(login_url="/login")
def producEsperados(request, id_proyecto, id_objetivoEsp):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    objGeneral = Objetivos.objects.get(proyecto=id_proyecto)
    objEspecifico = Objetivos_especificos.objects.get(objetivoGeneral=objGeneral, id=id_objetivoEsp)
    productoEsp = get_or_none(Resultados_y_productos_esperados, objetivo_especifico=objEspecifico.id)
    try:
        fecha_entrega = productoEsp.fch_entrega_producto_resultado_inv_obj_especifico.strftime('%Y-%m-%d')
    except:
        fecha_entrega = None
    if request.method == 'POST':
        form = ProducEsperadosForm(request.POST, instance=productoEsp)
        if form.is_valid():
            produc = form.save(commit=False)
            produc.objetivo_especifico_id = objEspecifico.id
            produc.save()
            return redirect("seleccionarObjetivo", id_proyecto)
    form = ProyectoForm()
    contex = {'percentaje':id_proyecto,
              'objEspecifico':objEspecifico,
              'productosEsp':productoEsp,
              'fecha':fecha_entrega}
    return render(request, 'form/producEsperados.html', contex)


@login_required(login_url="/login")
def proyeccion(request, id_proyecto):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    proyeccion = get_or_none(Proyeccion, proyecto=id_proyecto)
    try:
        fch_inicio = proyeccion.fch_inicio.strftime('%Y-%m-%d')
        fch_cierre = proyeccion.fch_cierre.strftime('%Y-%m-%d')
    except:
        fch_inicio = None
        fch_cierre = None
    contex = {
        "percentaje": id_proyecto,
        "proyecto": get_or_none(Proyecto, id=id_proyecto),
        "proyeccion": proyeccion,
        "fch_inicio":fch_inicio,
        "fch_cierre":fch_cierre
    }
    return render(request, "form/proyeccion.html", contex)


@login_required(login_url="/login")
def riesgo_general(request, id_proyecto):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    proyecto = get_or_none(Proyecto, id=id_proyecto)

    riesgos_g = get_or_none(RiesgoObjetivoGeneral, proyecto=id_proyecto)
    riesgos_p = get_or_none(RiesgoProductos, proyecto=id_proyecto)
    riesgos_a = get_or_none(RiesgoActividades, proyecto=id_proyecto)

    context = {
        "proyecto": proyecto,
        "riesgos_g": riesgos_g,
        "riesgos_p": riesgos_p,
        "riesgos_a": riesgos_a,
        "percentaje": id_proyecto,
    }

    return render(request, "form/riesgosp.html", context)


@login_required(login_url="/login")
def Informacion_de_centro(request, id_proyecto):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    if request.method == "POST":
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

    form = Informacion_proponenteForm(initial={"proyecto": proyecto})
    context = {"form": form, "proyecto": proyecto, "percentaje": id_proyecto}
    return render(request, "form/infop.html", context)


@login_required()   
def seleccionar(request,  id_proyecto):
    if not own_user(request.user, id_proyecto):
        return redirect(index)
    contex = {
        'percentaje' : 0,
        'id_proyecto' : id_proyecto,
    }
    return render(request, 'select_edit.html', contex)

  
#------JSON------
def info_proponente(request, id_proyecto):
    try:
        informacion_proponente = Informacion_proponente.objects.get(
            proyecto=id_proyecto
        )
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        informacion_proponente = Informacion_proponente.objects.create(
            proyecto=proyecto
        )
    model = Informacion_proponente
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue
        setattr(informacion_proponente, name, request.POST.get(name))
    try:
        informacion_proponente.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_autores(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    id_autor = request.POST.get('id_autor', None)
    if id_autor:
        autores = Autores.objects.get(id=id_autor)
    else:
        autores = Autores(proyecto=proyecto)

    model = Autores
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue

        setattr(autores, name, request.POST.get(name))
    try:
        autores.save()
        autoresG = Autores.objects.filter(proyecto = id_proyecto)
        # Obtener todas las entidades actualizadas
        nueva_lista_autores = []
        for autor in autoresG:
            nuevo_autor = {
                "id": autor.id,
                "nombre_Autor_Proyecto": autor.nombre_Autor_Proyecto,
                "tipo_Vinculacion_entidad": autor.tipo_Vinculacion_entidad,
                "numero_Cedula_Autor": autor.numero_Cedula_Autor,
                "rol_Sennova_De_Participantes_de_Proyecto": autor.rol_Sennova_De_Participantes_de_Proyecto,
                "email_Autor_Proyecto": autor.email_Autor_Proyecto,
                "numero_meses_vinculacion_Autor": autor.numero_meses_vinculacion_Autor,
                "numero_Telefono_Autor": autor.numero_Telefono_Autor,
                "numero_horas_Semanales_dedicadas_Autores": autor.numero_horas_Semanales_dedicadas_Autores
            }
            nueva_lista_autores.append(nuevo_autor)
        return JsonResponse({"mensaje": "Operación exitosa", "autores": nueva_lista_autores})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_participantes(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    id_participante = request.POST.get('id_participante', None)
    if id_participante:
        participante = Participantes_Proyecto.objects.get(id=id_participante)
    else:
        participante = Participantes_Proyecto(proyecto=proyecto)
    model = Participantes_Proyecto
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue

        setattr(participante, name, request.POST.get(name))
    try:
        participante.save()
        participantes = Participantes_Proyecto.objects.filter(proyecto = id_proyecto)
        # Obtener todas las entidades actualizadas
        nueva_lista_participantes = []
        for participante in participantes:
            nuevo_participante = {
                "id": participante.id,
                "nombre_participantes_de_desarrollo":participante.nombre_participantes_de_desarrollo,
                "numero_cedula_participantes": participante.numero_cedula_participantes,
                "numero_meses_vinculacion_participantes": participante.numero_meses_vinculacion_participantes,
                "email_participantes_de_desarrollo": participante.email_participantes_de_desarrollo,
                "numero_horas_Semanales_dedicadas_participantes": participante.numero_horas_Semanales_dedicadas_participantes,
                "numero_Telefono_participantes": participante.numero_Telefono_participantes
                }
            nueva_lista_participantes.append(nuevo_participante)
        return JsonResponse({"mensaje": "Operación exitosa", "participantes": nueva_lista_participantes})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_generalidades(request, id_proyecto):
    try:
        generalidades = Generalidades_del_proyecto.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        generalidades = Generalidades_del_proyecto.objects.create(proyecto=proyecto)

    preguntas = PreguntasP.objects.all()

    #Recorro todas las preguntas creadas para luego comprobar si la ID de la respuesta coincide con la pregunta y asi asociarla correctamente
    for pregunta in preguntas:
        if str(pregunta.id) in request.POST and request.POST[str(pregunta.id)]:
            try:
                respuesta = Respuestas.objects.get(pregunta_id=pregunta.id)
            except:
                respuesta = Respuestas()
            respuesta.respuesta = deleteSpacesInText(request.POST[str(pregunta.id)])
            respuesta.generalidad_id = generalidades.id
            respuesta.pregunta_id = pregunta.id
            respuesta.save()
        #Si le ID de la pregunta no llego es porque el usuario selecciono que no, por ende en caso de que exista hay que borrarla.
        if not str(pregunta.id) in request.POST and Respuestas.objects.filter(pregunta_id=pregunta.id).exists():
            Respuestas.objects.get(pregunta_id=pregunta.id).delete()

        

    model = Generalidades_del_proyecto
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue

        setattr(generalidades, name, request.POST.get(name))
    try:
        generalidades.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def getRegionJson(request):
    centross = list(Centro_formacion.objects.all().order_by('codigo').values())
    i = 0
    for item in centross:
        i=1+i
    return JsonResponse(
            {
                "mensaje": "Operación exitosa",
                "regiones": list(Region.objects.all().values()),
                "regionales": list(Regional.objects.all().order_by('nombre').values()),
                "centros": list(Centro_formacion.objects.all().order_by('codigo').values())
            }
        )


def resumen_antecedentes(request, id_proyecto):
    try:
        resumen = Resumen_antecedentes.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        resumen = Resumen_antecedentes.objects.create(proyecto=proyecto)
    resumen.resumen_ejecutivo = deleteSpacesInText(request.POST["Resumen_ejecutivo"])
    resumen.antecedentes = deleteSpacesInText(request.POST["Antecedentes"])
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
    descripcion.identificacion_y_descripcion_problema = deleteSpacesInText(request.POST["Identificacion_y_descripcion_problema"])
    descripcion.justificacion = deleteSpacesInText(request.POST["Justificacion"])
    descripcion.marco_conceptual = deleteSpacesInText(request.POST["Marco_conceptual"])

    try:
        descripcion.save()
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
        if name == "id" or name == "proyecto":
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
        if name == "id" or name == "proyecto":
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
        if name == "id" or name == "proyecto":
            continue
        setattr(riesgo_a_json, name, request.POST.get(name))
    try:
        riesgo_a_json.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

def objetivos_json(request, id_proyecto):
    try:
        objetivo = Objetivos.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        objetivo = Objetivos.objects.create(proyecto=proyecto)
    objetivoEsp = Objetivos_especificos.objects.filter(objetivoGeneral=objetivo.id)
    objetivo.objetivo_general = request.POST['objetivo_general']
    objetivo.save()
    for i in range(0, 5):
        if request.POST.get(f'objetivo_especifico{i+1}'):
            try:
                objEsp = objetivoEsp[i]
                objEsp.objetivo_especifico = request.POST[f'objetivo_especifico{i+1}']
                objEsp.save()
            except:
                objEsp = Objetivos_especificos.objects.create(objetivoGeneral=objetivo)
                objEsp.objetivo_especifico = request.POST[f'objetivo_especifico{i+1}']
                objEsp.save()
    
    return JsonResponse({"mensaje": "Operación exitosa"})

def actividades_json(request, id_proyecto):
    objetivo = Objetivos.objects.get(proyecto=id_proyecto)
    objetivoEsp = Objetivos_especificos.objects.filter(objetivoGeneral=objetivo.id)
    for i in range(0, len(objetivoEsp)):
        objEsp = objetivoEsp[i]
        objEsp.actividades_obj_especificos = request.POST[f'actividad{i+1}']
        objEsp.causa = request.POST[f'causa{i+1}']
        objEsp.efecto = request.POST[f'efecto{i+1}']
        objEsp.save()
        
    return JsonResponse({"mensaje": "Operación exitosa"})
    
    
def centro_formacion(request, id_proyecto):
    try:
        centro_f = Centro_de_formacion.objects.get(proyecto_id=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        centro_f = Centro_de_formacion.objects.create(proyecto=proyecto)

    model = Centro_de_formacion
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue

        setattr(centro_f, name, request.POST.get(name))

    try:
        centro_f.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def entidad_aliada(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    objGen = Objetivos.objects.filter(proyecto=proyecto.id).first()
    objsEsp = Objetivos_especificos.objects.filter(objetivoGeneral=objGen.id)
    array_booleanos = json.loads(request.POST['objetivo_especificos_relacionados'])
    id_entidad = request.POST.get('id_entidad', None)
    if id_entidad:
        entidad = Entidades_aliadas.objects.get(id=id_entidad)
    else:
        entidad = Entidades_aliadas(proyecto=proyecto)

    entidad.save()
    for indice, objetivoUwU in enumerate(objsEsp, start=1):
        if array_booleanos[indice - 1]:
            entidad.objetivo_especificos.add(objetivoUwU.id)

    model = Entidades_aliadas
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto" or name == "objetivo_especificos":
            continue
        setattr(entidad, name, request.POST.get(name))
    try:
        entidad.save()
        entidades = Entidades_aliadas.objects.filter(proyecto = proyecto)
        # Obtener todas las entidades actualizadas
        nueva_lista_entidades = []
        for entidadC in entidades:
            nueva_entidad = {}
            for name in column_names:
                if name == "proyecto" or name == "objetivo_especificos":
                    continue
                nueva_entidad[name] = getattr(entidadC, name)
            nueva_lista_entidades.append(nueva_entidad)
        return JsonResponse({"mensaje": "Operación exitosa", "entidades": nueva_lista_entidades})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def participantes_entidad_aliada(request, id_proyecto):
    id_entidad = request.POST["id_entidad"]
    entidad = Entidades_aliadas.objects.get(id=id_entidad)
    participante = Participantes_entidad_alidad(entidad=entidad)

    model = Participantes_entidad_alidad
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "entidad":
            continue

        setattr(participante, name, request.POST.get(name))
    try:
        participante.save()
        return JsonResponse(
            {
                "mensaje": "Operación exitosa",
                "nuevo_participante": {
                    "nombre": participante.nombre,
                    "numero_identificacion": participante.numero_identificacion,
                    "email": participante.email,
                    "telefono": participante.telefono,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def tiempo_ejecucion(request, id_proyecto):
    try:
        tiempo = Proyeccion.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        tiempo = Proyeccion.objects.create(proyecto=proyecto)
    tiempo.duracion = request.POST["duracion"]
    tiempo.fch_inicio = request.POST["fch_inicio"]
    tiempo.fch_cierre = request.POST["fch_cierre"]
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
    cadena.propuesta_sostenibilidad = deleteSpacesInText(request.POST["Propuesta_sostenibilidad"])
    cadena.impacto_social = deleteSpacesInText(request.POST["Impacto_social"])
    cadena.impacto_tecnologico = deleteSpacesInText(request.POST["Impacto_tecnologico"])
    cadena.impacto_centro_formacion = deleteSpacesInText(request.POST["Impacto_centro"])
    try:
        cadena.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ------Editar proyecto------
def edit_proyect(request, id_proyecto):
    user = request.user
    proyecto = Proyecto.objects.filter(id=id_proyecto).first()
    if not own_user(user, proyecto.id):
        return redirect(index)
    if request.method == "POST":
        model = Proyecto
        column_names = [field.name for field in model._meta.fields]

        for name in column_names:
            if name == "id" or name == "usuario" or name == 'titulo_Proyecto' or name == 'descripcion' or name == 'fecha_creacion':
                continue
            setattr(proyecto, name, request.POST.get(name))
        proyecto.titulo_Proyecto = deleteSpacesInText(request.POST.get('titulo_Proyecto'))
        proyecto.descripcion = deleteSpacesInText(request.POST.get('descripcion'))
        proyecto.save()

    context = {
        "proyecto": proyecto,
        "listaPlegable": contex_form(),
        "percentaje": id_proyecto,
    }
    return render(request, "edit_form/edit_proy.html", context)


def proyectos_usuario(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    contex = {
        'percentaje': 0,
        'proyectos': proyectos
    }
    return render(request, "proyectos.html", contex)

def recursos(request, id_proyecto):
    objGeneral = get_or_none(Objetivos, proyecto=id_proyecto)
    objEspecificos = Objetivos_especificos.objects.filter(objetivoGeneral=objGeneral.id)
    entidades = Entidades_aliadas.objects.filter(proyecto=id_proyecto)
    participantes = Participantes_entidad_alidad.objects.filter(entidad__in=entidades)
    contex = {'percentaje': id_proyecto,
              'objEspecificos':objEspecificos,
              'entidades':entidades,
              'participantes':participantes,
              'rubros':Rubro.objects.filter(estado=True).order_by('descripcion'),
              'tipoRubros':TipoRubro.objects.all().order_by('descripcion')}
    return render(request, 'form/recursos.html', contex)

def presupuestoJson(request, id_proyecto, id_actividad):
    try:
        presupuesto = Presupuesto.objects.get(actividad=id_actividad)
        presupuesto.actividad = request.POST.get('actividadR')
        presupuesto.tipoRubro = request.POST.get('tipo_rubro')
        presupuesto.valor = request.POST.get('valor')
        presupuesto.rubro = valor=request.POST.get('rubro')
        presupuesto.save()
    except:
        actividad = Objetivos_especificos.objects.get(id=request.POST.get('actividadR'))
        tipoRubro = TipoRubro.objects.get(id=request.POST.get('tipo_rubro'))
        rubro = Rubro.objects.get(id=request.POST.get('rubro'))
        presupuesto = Presupuesto.objects.create(actividad=actividad,
                                                 tipoRubro=tipoRubro,
                                                 valor=request.POST.get('valor'),
                                                 rubro=rubro
                                                 )
    try:
        presupuesto.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def cronogramaJson(request, id_proyecto, id_actividad):
    entidades = Entidades_aliadas.objects.filter(proyecto=id_proyecto)
    participantes = Participantes_entidad_alidad.objects.filter(entidad__in=entidades)
    try:
        cronograma = CronogramaAct.objects.get(actividad=id_actividad)
    except:
        actividad = Objetivos_especificos.objects.get(id=id_actividad)
        cronograma = CronogramaAct.objects.create(actividad=actividad)

    cronograma.save()
    

    array_booleanos_entidad = json.loads(request.POST['actorEntidad'])
    array_booleanos_participantes = json.loads(request.POST['actorPartipantes'])
    for indice, entidadUwU in enumerate(entidades, start=1):
        if array_booleanos_entidad[indice - 1]:
            cronograma.actorEntidad.add(entidadUwU.id)
    
    for indice, participanteUwU in enumerate(participantes, start=1):
        if array_booleanos_participantes[indice - 1]:
            cronograma.actorParticipante.add(participanteUwU.id)

    model = CronogramaAct
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "actividad":
            continue

        setattr(cronograma, name, request.POST.get(name))
    try:
        cronograma.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    
@csrf_exempt
def gantt_data(request):
    if request.method == 'GET':
        data = []

        objetivos_especificos = Objetivos_especificos.objects.all()

        for objetivo in objetivos_especificos:
            cronograma = objetivo.cronogramaact

            if cronograma:

                data.append({
                    "id": objetivo.id,
                    "text": objetivo.actividades_obj_especificos,
                    "start_date": datetime.strftime(cronograma.fch_inicio, "%Y-%m-%d"),
                    "duration": (cronograma.fch_cierre - cronograma.fch_inicio).days + 1,
                })
        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
## Funciones de anexo
def anexos(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    documentos = Document.objects.filter(estado=True)

    contex = {
        'percentaje' : id_proyecto,
        'id_proyecto': id_proyecto,
        'documentos': documentos,
    }
    
    return render(request, 'form/anexos.html', contex)

## Hola este es de subir
@csrf_exempt
def subir_anexo(request):
    if request.method == 'POST':
        try:
            proyecto_id = request.POST.get('proyecto_id')
            documentos = Document.objects.all()

            archivos_subidos = 0
            for documento in documentos:
                nombre_input = 'anexo_' + str(documento.id)
                if nombre_input in request.FILES:
                    archivo = request.FILES[nombre_input]
                    if Anexos.objects.filter(anexo_requerido=documento.id, proyecto_id=proyecto_id).exists():
                        anexo = Anexos.objects.filter(anexo_requerido=documento.id, proyecto_id=proyecto_id)
                        anexo.anexo=archivo
                        print(anexo)
                    else:
                        anexo = Anexos(anexo_requerido=documento, proyecto_id=proyecto_id, anexo=archivo)
                        print(anexo)
                    anexo.save()
                    archivos_subidos += 1

            if archivos_subidos > 0:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'No se han enviado archivos'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def obtener_id_anexo_requerido(nombre_anexo_requerido):
    try:
        anexo_requerido = Anexos.objects.get(anexo_requerido=nombre_anexo_requerido)
        return anexo_requerido.id
    except Anexos.DoesNotExist:
        return None

def descargar_guia(request, documento_id):
    documento = get_object_or_404(Document, pk=documento_id)
    if documento.guia:
        # Abrir el archivo y leer su contenido
        with open(documento.guia.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{documento.guia.name}"'
            return response
    else:
        # Si no hay guía disponible, regresar un mensaje de error
        return HttpResponse('El documento guía no está disponible', status=404)
    
def descargar_anexo(request, anexo_id):
    try:
        anexo = Anexos.objects.get(pk=anexo_id)
        file_path = os.path.join(settings.MEDIA_ROOT, str(anexo.anexo))
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    except Anexos.DoesNotExist:
        return HttpResponse('Anexo no encontrado', status=404)
    except Exception as e:
        return HttpResponse(str(e), status=500)
    
    
def pdfnuevo(request, proyecto_id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Reporte.pdf"'
    buffer = BytesIO()
    
    # Creamos un documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    Story = []
    
    # Definimos el estilo para los párrafos
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    
    # Agregamos el marco para el texto
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.5*inch, id='normal')
    template = PageTemplate(id='test', frames=[frame])
    doc.addPageTemplates([template])

    # Creamos el texto para el número de página
    def numero_pagina(canvas, doc):
        numero = canvas.getPageNumber()
        canvas.setFont("Helvetica", 8)
        texto = "Página %d" % numero
        canvas.drawRightString(doc.width - 20, 20, texto)
    

    template.afterDrawPage = numero_pagina
    
    # Obtener el proyecto y los datos relacionados
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    documentos_anexos = Anexos.objects.filter(proyecto=proyecto)
    
    # Función para agregar secciones con título y contenido
    def agregar_seccion(titulo, contenido):
        Story.append(Paragraph(titulo, styles["Heading2"]))
        Story.append(Spacer(1, 12))
        paragraphs = contenido.split("\n")
        for paragraph in paragraphs:
            Story.append(Paragraph(paragraph, normal_style))
        Story.append(Spacer(1, 12))
    
    # Agregar título al documento
    Story.append(Paragraph("Reporte general", styles["Title"]))
    Story.append(Spacer(1, 12))
    negrita_style = ParagraphStyle('Negrita', parent=normal_style, fontName='Helvetica-Bold')
    
   # Informacion proyecto
    proyecto_info = Proyecto.objects.get(id=proyecto_id)
    proyecto_info_str = f"<b>Título del proyecto:</b> {proyecto_info.titulo_Proyecto}\n"\
                        f"<b>Descripción:</b> {proyecto_info.descripcion}\n" \
                        f"<b>Código Grupo de Investigación:</b> {proyecto_info.codigo_Grupo_Investigacion}\n" \
                        f"<b>Red de Conocimiento Sectorial:</b> {proyecto_info.red_Conocimiento_Sectorial}\n" \
                        f"<b>Disciplina Subárea:</b> {proyecto_info.disciplina_subarea}\n" \
                        f"<b>Nombre Grupo de Investigación:</b> {proyecto_info.nombre_Grupo_Investigacion}\n" \
                        f"<b>Área Conocimiento:</b> {proyecto_info.area_conocimiento}\n" \
                        f"<b>Línea Grupo de Investigación:</b> {proyecto_info.linea_Grupo_Investigacion}\n" \
                        f"<b>Subárea Conocimiento:</b> {proyecto_info.subarea_conocimiento}\n" \
                        f"<b>Fecha de Creación:</b> {proyecto_info.fecha_creacion.strftime('%d/%m/%Y')}"
    agregar_seccion("Proyecto", proyecto_info_str)
    
    # Informacion Proponente    
    proponente_info = Informacion_proponente.objects.filter(proyecto=proyecto)
    if proponente_info.exists():
        proponente_info_str = ""
        for info in proponente_info:
            proponente_info_str += f"<b>Región:</b> {info.Region}\n" \
                                    f"<b>Regional:</b> {info.Regional}\n" \
                                    f"<b>Nombre Centro de Formación:</b> {info.Nombre_centro_formacion}\n" \
                                    f"<b>Nombre Director:</b> {info.Nombre_Director}\n" \
                                    f"<b>Número Director:</b> {info.Numero_Director}\n" \
                                    f"<b>Email Director:</b> {info.email_director}\n" \
                                    f"<b>Nombre Sub Director:</b> {info.Nombre_Sub_Director}\n" \
                                    f"<b>Número Sub Director:</b> {info.Numero_Sub_Director}\n" \
                                    f"<b>Email Sub Director:</b> {info.email_sub_director}\n\n"
        agregar_seccion("Información del proponente", proponente_info_str)
    
    # Autores
    autor_info = Autores.objects.filter(proyecto=proyecto)
    if autor_info.exists():
        autor_info_str = ""
        for auto in autor_info:
            autor_info_str += f"<b>Nombre de autor:</b> {auto.nombre_Autor_Proyecto}\n" \
                                f"<b>Tipo de vinculacion:</b> {auto.tipo_Vinculacion_entidad}\n" \
                                f"<b>Numero de cedula:</b> {auto.numero_Cedula_Autor}\n" \
                                f"<b>Rol sennova:</b> {auto.rol_Sennova_De_Participantes_de_Proyecto}\n"\
                                f"<b>email de autor:</b> {auto.email_Autor_Proyecto}\n"\
                                f"<b>Numero de meses de vinculacion:</b> {auto.numero_meses_vinculacion_Autor}\n"\
                                f"<b>telefono de autor:</b> {auto.numero_Telefono_Autor}\n"\
                                f"<b>Horas semanales:</b> {auto.numero_horas_Semanales_dedicadas_Autores}\n\n"
        agregar_seccion("Informacion de autores", autor_info_str)        
    
    # Generalidades del proyecto
    generalidades_info = Generalidades_del_proyecto.objects.filter(proyecto=proyecto)
    if generalidades_info.exists():
        generalidades_info_str = ""
        for info in generalidades_info:
            generalidades_info_str += f"<b>Código Dependencia Presupuestal:</b> {info.codigo_Dependencia_Presupuestal}\n" \
                                      f"<b>Tematicas y Estrategias SENA:</b> {info.tematicas_Estrategias_SENA}\n\n"
        agregar_seccion("Generalidades del proyecto", generalidades_info_str)
    
    # Resumen de antecedentes
    resumen_info = Resumen_antecedentes.objects.filter(proyecto=proyecto)
    if resumen_info.exists():
        resumen_info_str = ""
        for info in resumen_info:
            resumen_info_str += f"<b>Resumen Ejecutivo:</b> {info.resumen_ejecutivo}\n"\
                                f"<b>Antecedentes:</b> {info.antecedentes}\n\n"
        agregar_seccion("Resumen de antecedentes", resumen_info_str)
    
    # Descripción del problema
    descripcion_info = Descripcion_problema.objects.filter(proyecto=proyecto)
    if descripcion_info.exists():
        descripcion_info_str = ""
        for info in descripcion_info:
            descripcion_info_str += f"<b>Identificación y Descripción del Problema:</b> {info.identificacion_y_descripcion_problema}\n"\
                                    f"<b>Justificacion:</b> {info.justificacion}\n"\
                                    f"<b>Marco conceptual:</b> {info.marco_conceptual}\n\n"
        agregar_seccion("Descripción del problema", descripcion_info_str)
    
    
    # objetivos generales y específicos
    objetivos_generales = Objetivos.objects.filter(proyecto=proyecto)
    objetivos_especificos = Objetivos_especificos.objects.filter(objetivoGeneral__in=objetivos_generales)

    if objetivos_generales.exists():
        objetivos_generales_str = ""
        for objetivo_general in objetivos_generales:
            objetivos_generales_str += f"<b>Objetivo general:</b> {objetivo_general.objetivo_general}\n\n"
        agregar_seccion("Objetivo general", objetivos_generales_str)

    if objetivos_especificos.exists():
        objetivos_especificos_str = ""
        for objetivo_especifico in objetivos_especificos:
            objetivos_especificos_str += f"<b>Objetivo específico:</b> {objetivo_especifico.objetivo_especifico}\n" \
                                        f"<b>Actividades:</b> {objetivo_especifico.actividades_obj_especificos}\n" \
                                        f"<b>Causa:</b> {objetivo_especifico.causa}\n" \
                                        f"<b>Efecto:</b> {objetivo_especifico.efecto}\n\n"
        agregar_seccion("Objetivos específicos", objetivos_especificos_str)
    
    
    # Centro de formacion
    cen_formacion = Centro_de_formacion.objects.filter(proyecto=proyecto)
    if cen_formacion.exists():
        cen_formacion_str = ""
        for info_centro in cen_formacion:
            cen_formacion_str +=f"<b>Nombre de semillero de investigacion:</b> {info_centro.nombre_semillero_investigacion_beneficiados}\n"\
                                f"<b>Numero de programas beneficiados:</b> {info_centro.numero_programas_beneficiarios_semilleros_investigacion}\n"\
                                f"<b>Tipo de programas de formacion beneficiados del semillero:</b> {info_centro.tipo_programas_formacion_beneficiados_conforman_semillero}\n"\
                                f"<b>Nombre de programas beneficiados:</b> {info_centro.nombre_programas_formacion_beneficiados_semillero}\n"\
                                f"<b>Tipo de programas beneficiados por ejecucion:</b> {info_centro.tipo_programas_de_formacion_beneficiados_por_ejecucion}\n"\
                                f"<b>Nombre de los programas beneficiados por ejecucion:</b> {info_centro.nombre_programas_formacion_beneficiados_ejecucion_proyecto}\n"\
                                f"<b>Numero de aprendices que participaran en la ejecucion:</b> {info_centro.numero_aprendices_participaran_ejecucion_proyecto}\n"\
                                f"<b>Numero de municipios beneficiados:</b> {info_centro.numero_municipios_beneficiados}\n"\
                                f"<b>Nombre de los municipios beneficiados:</b> {info_centro.nombre_municipios_beneficiados_descripcion_beneficio}\n\n"
        agregar_seccion("Centro de formacion", cen_formacion_str)
    
    # Entidades aliadas
    enti_ali = Entidades_aliadas.objects.filter(proyecto= proyecto)
    if enti_ali.exists():
        enti_ali_str = ""
        for info_enti in enti_ali:
            enti_ali_str += f"<b>Nombre de la entidad:</b> {info_enti.nombre_entidad}\n"\
                            f"<b>Tipo de entidad aliada:</b> {info_enti.tipo_entidad_aliada}\n"\
                            f"<b>Naturaleza de la entidad:</b> {info_enti.naturaleza_entidad}\n"\
                            f"<b>Clasificacion de empresa:</b> {info_enti.clasificacion_empresa}\n"\
                            f"<b>Codigo NIT:</b> {info_enti.nit}\n"\
                            f"<b>Convenio:</b> {info_enti.convenio}\n"\
                            f"<b>Tipo de convenio:</b> {info_enti.especifique_tipo_codigo_convenio}\n"\
                            f"<b>Recursos en especie aportados:</b> {info_enti.recursos_especie_entidad}\n"\
                            f"<b>Descripcion de recursos en especie aportados:</b> {info_enti.descripcion_recursos_especie_aportados}\n"\
                            f"<b>Recursos en dinero aportados:</b> {info_enti.recursos_dinero_entidad_aliada}\n"\
                            f"<b>Descripcion de destinacion de dinero aportado:</b> {info_enti.descripcion_destinacion_dinero_aportado}\n"\
                            f"<b>Nombre de grupo de invistigacion de entidad aliada:</b> {info_enti.nombre_grupo_inv_entidad_aliada}\n"\
                            f"<b>Codigo de GrupoLAC:</b> {info_enti.codigo_gruplac_entidad_aliada}\n"\
                            f"<b>Link del GrupoLac:</b> {info_enti.link_gruplac_entidad_aliada}\n"\
                            f"<b>Actividades a desarrollar por la entidad aliada:</b> {info_enti.actividades_desarrollar_entidad_aliada_marco_proyecto}\n"
            
            objetivos_especificos = info_enti.objetivo_especificos.all()
            if objetivos_especificos.exists():
                enti_ali_str += "<b>Objetivos específicos relacionados:</b>\n"
                for obj_especifico in objetivos_especificos:
                    enti_ali_str += f"- {obj_especifico.objetivo_especifico}\n"
            else:
                enti_ali_str += "No hay objetivos específicos relacionados\n"
            
            enti_ali_str += "\n\n"
        agregar_seccion("Entidad aliada", enti_ali_str)

    # Participantes entidad alida
    part_enti = Participantes_entidad_alidad.objects.filter(entidad__in=enti_ali)
    if part_enti.exists():
        part_enti_str = ""
        for info_parti in part_enti:
            part_enti_str += f"<b>Nombre del participante:</b> {info_parti.nombre}\n"\
                             f"<b>Numero de identificacion del participante:</b> {info_parti.numero_identificacion}\n"\
                             f"<b>Email del participante:</b> {info_parti.email}\n"\
                             f"<b>Telefono del participante del participante:</b> {info_parti.telefono}\n\n"
        agregar_seccion("Participantes de entidad alida", part_enti_str)
        
        
    # Resultados y productos esperados
    produt_resul = Resultados_y_productos_esperados.objects.filter(objetivo_especifico__in=objetivos_especificos)
    if produt_resul.exists():
        produt_resul_str= ""
        for info_resul in produt_resul:
            produt_resul_str += f"<b>Tipo de resultado esperado:</b> {info_resul.tipo_resultado_esperado_obj_especifico}\n"\
                                f"<b>Descripcion de resultado esperado:</b> {info_resul.descripcion_resultado_esperado_obj_especifico}\n"\
                                f"<b>Nombre del producto resultado de la investigación objetivo específico:</b> {info_resul.nombre_producto_resultado_inv_obj_especifico}\n"\
                                f"<b>Nombre de la sub-tipologia:</b> {info_resul.nombre_subtipologia}\n"\
                                f"<b>TRL de producto resultado de investigacion:</b> {info_resul.trl_producto_resultado_inv_obj_especifico}\n"\
                                f"<b>Indicador del producto resultado de la investigación objetivo específico:</b> {info_resul.indicador_producto_resultado_inv_obj_especifico}\n"\
                                f"<b>Fecha de entrega del producto resultado de investigacion:</b> {info_resul.fch_entrega_producto_resultado_inv_obj_especifico}\n\n"
                                
        agregar_seccion("Resultados y productos esperados",produt_resul_str)
        
    
    # Proyeccion
    proyecc = Proyeccion.objects.filter(proyecto=proyecto)
    if proyecc.exists():
        proyecc_str = ""
        for info_pro in proyecc:
            proyecc_str += f"<b>Duracion:</b> {info_pro.duracion}\n"\
                           f"<b>Fecha de inicio:</b> {info_pro.fch_inicio}\n"\
                           f"<b>Fecha de cierre:</b> {info_pro.fch_cierre}\n"\
                           f"<b>Propuesta de sostenibilidad:</b> {info_pro.propuesta_sostenibilidad}\n"\
                           f"<b>Impacto Social:</b> {info_pro.impacto_social}\n"\
                           f"<b>Impacto Tecnologico:</b> {info_pro.impacto_tecnologico}\n"\
                           f"<b>Impacto en el centro de formacion:</b> {info_pro.impacto_centro_formacion}\n\n"
        agregar_seccion("Proyeccion",proyecc_str)
    
    # Anexos                
    documentos_anexos = Anexos.objects.filter(proyecto=proyecto)

    if documentos_anexos.exists():
        for anexo in documentos_anexos:
            documento_requerido = anexo.anexo_requerido.nombre if anexo.anexo_requerido else "No disponible"
            info_anexo = f"<b>Documento requerido:</b> {documento_requerido}\n"
            if anexo.anexo:
                info_anexo += f"<b>Nombre del anexo:</b> {anexo.anexo.name}\n"
            else:
                info_anexo += "Anexo no subido\n"
            agregar_seccion("Anexo", info_anexo)
    else:
        agregar_seccion("Documentos y Anexos", "No hay documentos ni anexos asociados")
    
    doc.build(Story)
    
    # Obtener el contenido del buffer y enviar la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response