from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse

from app.forms import (
    Informacion_proponenteForm,
    ObjetivoEspecificoForm,
    ProyectoForm,
    ObjetivoForm,
    DocumentForm,
    ProducEsperados,
    ParticipantesEntidadForm,
)
from app.models import (
    Arbol_de_Objetivos,
    Entidades_aliadas,
    Proyecto,
    Informacion_proponente,
    Generalidades_del_proyecto,
    Participantes_Proyecto,
    Autores,
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
)


from django.contrib.auth.decorators import login_required
from app.views.index import index

# Listas desplegables
from app.models import Listas_plegables

import datetime
import os
import json

# PDF
from django.template.loader import render_to_string
from xhtml2pdf import pisa


# ------Decoradores------
def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list("rol", flat=True))
    required_roles = set(roles)

    return bool(user_roles & required_roles)


# ------Funciones generales------
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
    codigos = lista.order_by("codigos_grupo_investigacion").values_list(
        "codigos_grupo_investigacion", flat=True
    )
    nombres = lista.order_by("nombre_grupo_investigacion").values_list(
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
    return {
        "codigos": codigos,
        "nombres": nombres,
        "redes": redes,
        "subareas": subareas,
        "diciplinas": diciplinas,
        "nombresC": nombresC,
    }


# def generar_pdf(request, proyecto_id):

#     proyecto = Proyecto.objects.get(id=proyecto_id)
#     informacion_proponente = Informacion_proponente.objects.get(proyecto=proyecto)
#     autores = Autores.objects.filter(proyecto=proyecto)
#     part_p = Participantes_Proyecto.objects.filter(proyecto=proyecto)
#     gen = Generalidades_del_proyecto.objects.filter(proyecto=proyecto.id).first()
#     res = Resumen_antecedentes.objects.filter(proyecto=proyecto.id).first()
#     des_p = Descripcion_problema.objects.filter(proyecto=proyecto.id).first()
#     objg = Objetivos.objects.filter(proyecto=proyecto.id).first()
#     obje = Objetivos_especificos.objects.filter(objetivos=objg.id).first()
#     print(obje)
#     acte = Actividades_de_objetivos_especificos.objects.filter(objetivo_especificos=obje.id).first()
#     causa = Causa.objects.filter(objetivo_e=obje.id).first()
#     efecto = Efecto.objects.filter(causa=causa.id).first()
#     centro_f = Centro_de_formacion.objects.filter(proyecto=proyecto.id).first()
#     entidad_a= Entidades_aliadas.objects.filter(proyecto=proyecto)


#     # Renderizar el template con los datos
#     context = {
#         'proyecto': proyecto,
#         'informacion_proponente': informacion_proponente,
#         'autores': autores,
#         'part_p': part_p,
#         'gen': gen,
#         'res': res,
#         'des_p': des_p,
#         'objg': objg,
#         'obje': obje,
#         'acte': acte,
#         'causa': causa,
#         'efecto': efecto,
#         'centro_f': centro_f,
#         'entidad_a': entidad_a,
#     }

#     template_path = 'form/informe.html'
#     html = render_to_string(template_path, context)

#     # Lógica para generar el informe PDF a partir del HTML con xhtml2pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=informe_general.pdf'

#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse('Error al generar el PDF', status=500)

#     return response


def generar_pdf(request, proyecto_id):
    # Obtener el proyecto y otros datos relacionados
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    informacion_proponente = get_or_none(Informacion_proponente, proyecto=proyecto.id)
    autores = Autores.objects.filter(proyecto=proyecto)
    part_p = Participantes_Proyecto.objects.filter(proyecto=proyecto)
    gen = Generalidades_del_proyecto.objects.filter(proyecto=proyecto).first()
    res = Resumen_antecedentes.objects.filter(proyecto=proyecto).first()
    des_p = Descripcion_problema.objects.filter(proyecto=proyecto).first()
    proy = Proyeccion.objects.filter(proyecto=proyecto).first()
    riesgo_g = RiesgoObjetivoGeneral.objects.filter(proyecto=proyecto).first()
    riesgo_p = RiesgoProductos.objects.filter(proyecto=proyecto).first()
    riesgo_a = RiesgoActividades.objects.filter(proyecto=proyecto).first()
    objetivos = Objetivos.objects.filter(proyecto=proyecto).first()
    objetivos_especificos = Objetivos_especificos.objects.filter(objetivos=objetivos).all()
    arboles_objetivos = Arbol_de_Objetivos.objects.filter(
        objetivo_especificos__in=objetivos_especificos
    ).all()
    doc = Document.objects.filter(proyecto=proyecto).first()
    resultados_productos_esperados = Resultados_y_productos_esperados.objects.filter(
        objetivo_especifico__objetivos__proyecto=proyecto
    )


    centro_f = Centro_de_formacion.objects.filter(proyecto=proyecto).first()
    entidad_a = Entidades_aliadas.objects.filter(proyecto=proyecto)
    partp_e = {}
    for entidad_aliada in entidad_a:
        participantes_entidad_aliada = Participantes_entidad_alidad.objects.filter(
            entidad=entidad_aliada
        )
        partp_e[entidad_aliada] = participantes_entidad_aliada
    
    # Renderizar el template con los datos
    context = {
        "proyecto": proyecto,
        "informacion_proponente": informacion_proponente,
        "autores": autores,
        "part_p": part_p,
        "gen": gen,
        "res": res,
        "des_p": des_p,
        "centro_f": centro_f,
        "entidad_a": entidad_a,
        "proy": proy,
        "riesgo_g": riesgo_g,
        "riesgo_p": riesgo_p,
        "riesgo_a": riesgo_a,
        "doc": doc,
        "partp_e": partp_e,
        'objetivos': objetivos,
        'objetivos_especificos': objetivos_especificos,
        'arboles_objetivos': arboles_objetivos,
        "resultados_productos_esperados": resultados_productos_esperados,
    }

    template_path = "form/informe.html"
    html = render_to_string(template_path, context)

    # Lógica para generar el informe PDF a partir del HTML con xhtml2pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=informe_general.pdf"

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

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
            proyecto.usuario = request.user
            proyecto.progress = 10
            proyecto.save()
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
    context = {
        "proyecto": get_or_none(Proyecto, id=id_proyecto),
        "infoProyecto": Informacion_proponente.objects.filter(
            proyecto_id=get_or_none(Proyecto, id=id_proyecto)
        ).first(),
        "autores": Autores.objects.filter(proyecto=proyecto),
        "participantes": Participantes_Proyecto.objects.filter(proyecto=proyecto),
        "percentaje": id_proyecto,
        "listaPlegable": contex_form(),
    }
    return render(request, "form/infop.html", context)


@login_required(login_url="/login")
def estructura_proyecto(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    if not own_user(request.user, proyecto.id):
        return redirect(index)
    context = {
        "proyecto": proyecto,
        "resumen": get_or_none(Resumen_antecedentes, proyecto=proyecto),
        "percentaje": id_proyecto,
    }
    return render(request, "form/estp.html", context)


@login_required(login_url="/login")
def crear_objetivo(request, objetivo_proyecto_id):
    if not own_user(request.user, get_or_none(Proyecto, id=objetivo_proyecto_id).id):
        return redirect(index)
    contex = {
        "percentaje": objetivo_proyecto_id,
    }
    return render(request, "form/objetivos.html", contex)


@login_required(login_url="/login")
def participantes(request, id_proyecto):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    objGeneral = Objetivos.objects.get(proyecto=proyecto.id)
    context = {
        "proyecto": proyecto,
        "entidad_a": Entidades_aliadas.objects.filter(proyecto=proyecto),
        "centro_f": Centro_de_formacion.objects.filter(proyecto=proyecto),
        "objEspecificos": Objetivos_especificos.objects.filter(objetivos=objGeneral),
        "percentaje": id_proyecto,
    }
    return render(request, "form/partp.html", context)


@login_required(login_url="/login")
def selecEntidad(request, id_proyecto):
    proyecto = get_or_none(Proyecto, id=id_proyecto)
    if not own_user(request.user, proyecto.id):
        return redirect(index)
    if not Entidades_aliadas.objects.filter(proyecto=proyecto).exists():
        return HttpResponse(
            "Para acceder a esta vista debes de crear por lo menos una entidad aliada"
        )
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
        objEspecificos = Objetivos_especificos.objects.filter(objetivos_id=objGeneral)
    except:
        return HttpResponse(
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
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    objGeneral = Objetivos.objects.get(proyecto=id_proyecto)
    objEspecifico = Objetivos_especificos.objects.get(
        objetivos_id=objGeneral, id=id_objetivoEsp
    )
    if request.method == "POST":
        form = ProducEsperados(request.POST)
        if form.is_valid():
            produc = form.save(commit=False)
            produc.objetivo_especifico_id = objEspecifico.id
            produc.save()
            return redirect("seleccionarObjetivo", id_proyecto)
    form = ProyectoForm()
    contex = {"percentaje": id_proyecto, "objEspecifico": objEspecifico}
    return render(request, "form/producEsperados.html", contex)


@login_required(login_url="/login")
def proyeccion(request, id_proyecto):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
        return redirect(index)
    contex = {
        "percentaje": id_proyecto,
        "proyecto": get_or_none(Proyecto, id=id_proyecto),
    }
    return render(request, "form/proyeccion.html", contex)


@login_required(login_url="/login")
def riesgo_general(request, id_proyecto):
    if not own_user(request.user, get_or_none(Proyecto, id=id_proyecto).id):
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


@login_required(login_url="/login")
def subir_anexos(request, proyecto_id):
    if not own_user(request.user, get_or_none(Proyecto, id=proyecto_id).id):
        return redirect(index)
    proyecto = get_or_none(Proyecto, pk=proyecto_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            anexo = form.save(commit=False)
            anexo.proyecto = proyecto
            anexo.save()

    documents = Document.objects.filter(proyecto=proyecto)
    contex = {"docs": documents, "proyecto": proyecto, "percentaje": proyecto_id}
    return render(request, "form/anexos.html", contex)


# ------JSON------
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
    autores = Autores(
        proyecto=proyecto
    )  # Crea una nueva instancia en lugar de obtener una existente

    model = Autores
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue

        setattr(autores, name, request.POST.get(name))
    try:
        autores.save()
        return JsonResponse(
            {
                "mensaje": "Operación exitosa",
                "nuevo_autor": {
                    "nombre_Autor_Proyecto": autores.nombre_Autor_Proyecto,
                    "tipo_Vinculacion_entidad": autores.tipo_Vinculacion_entidad,
                    "numero_Cedula_Autor": autores.numero_Cedula_Autor,
                    "rol_Sennova_De_Participantes_de_Proyecto": autores.rol_Sennova_De_Participantes_de_Proyecto,
                    "email_Autor_Proyecto": autores.email_Autor_Proyecto,
                    "numero_Telefono_Autor": autores.numero_Telefono_Autor,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def info_participantes(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    participante = Participantes_Proyecto(proyecto=proyecto)

    model = Participantes_Proyecto
    column_names = [field.name for field in model._meta.fields]

    for name in column_names:
        if name == "id" or name == "proyecto":
            continue

        setattr(participante, name, request.POST.get(name))
    try:
        participante.save()
        return JsonResponse(
            {
                "mensaje": "Operación exitosa",
                "nuevo_participante": {
                    "nombre_participantes_de_desarrollo": participante.nombre_participantes_de_desarrollo,
                    "numero_cedula_participantes": participante.numero_cedula_participantes,
                    "numero_meses_vinculacion_participantes": participante.numero_meses_vinculacion_participantes,
                    "email_participantes_de_desarrollo": participante.email_participantes_de_desarrollo,
                    "numero_horas_Semanales_dedicadas_participantes": participante.numero_horas_Semanales_dedicadas_participantes,
                    "numero_Telefono_participantes": participante.numero_Telefono_participantes,
                },
            }
        )
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
        if name == "id" or name == "proyecto":
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


def resumen_antecedentes(request, id_proyecto):
    try:
        resumen = Resumen_antecedentes.objects.get(proyecto=id_proyecto)
    except:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        resumen = Resumen_antecedentes.objects.create(proyecto=proyecto)
    resumen.resumen_ejecutivo = request.POST["Resumen_ejecutivo"]
    resumen.antecedentes = request.POST["Antecedentes"]
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
    descripcion.identificacion_y_descripcion_problema = request.POST[
        "Identificacion_y_descripcion_problema"
    ]
    descripcion.justificacion = request.POST["Justificacion"]
    descripcion.marco_conceptual = request.POST["Marco_conceptual"]

    try:
        descripcion.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
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
        if name == "id" or name == "proyecto":
            continue

        setattr(centro_f, name, request.POST.get(name))

    try:
        centro_f.save()
        # print("Guardado exitosamente")
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def entidad_aliada(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    objGen = Objetivos.objects.filter(proyecto=proyecto.id).first()
    objsEsp = Objetivos_especificos.objects.filter(objetivos=objGen.id)
    array_booleanos = json.loads(request.POST["objetivo_especificos_relacionados"])

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
        return JsonResponse(
            {
                "mensaje": "Operación exitosa",
                "nueva_entidad": {
                    "nombre_entidad": entidad.nombre_entidad,
                    "tipo_entidad_aliada": entidad.tipo_entidad_aliada,
                    "naturaleza_entidad": entidad.naturaleza_entidad,
                    "clasificacion_empresa": entidad.clasificacion_empresa,
                    "nit": entidad.nit,
                },
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def participantes_entidad_aliada(request, id_proyecto):
    id_entidad = request.POST["id_entidad"]
    proyecto = Proyecto.objects.get(id=id_proyecto)
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
    cadena.cadena_valor = request.FILES["Cadena_valor"]
    cadena.propuesta_sostenibilidad = request.POST["Propuesta_sostenibilidad"]
    cadena.impacto_social = request.POST["Impacto_social"]
    cadena.impacto_tecnologico = request.POST["Impacto_tecnologico"]
    cadena.impacto_centro_formacion = request.POST["Impacto_centro"]
    try:
        cadena.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---FIN YEISON ---


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
            if name == "id" or name == "usuario":
                continue
            setattr(proyecto, name, request.POST.get(name))
        proyecto.save()

    context = {
        "proyecto": user.proyecto_set.first(),
        "listaPlegable": contex_form(),
        "percentaje": id_proyecto,
    }
    return render(request, "edit_form/edit_proy.html", context)


def editar_anexo(request, proyecto_id):
    try:
        proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
        anexo = Document.objects.filter(proyecto=proyecto).first()
        print(anexo)
    except:
        return redirect("subir_anexos", proyecto_id)

    if request.method == "POST":
        model = Document
        column_names = [field.name for field in model._meta.fields]

        for name in column_names:
            if (
                name == "id"
                or name == "fecha"
                or name == "proyecto_id"
                or request.FILES.get(name) == None
            ):
                continue
            setattr(anexo, name, request.FILES.get(name))
        anexo.save()

    form = DocumentForm()
    return render(
        request,
        "edit_form/edit_anexos.html",
        {"form": form, "proyecto": proyecto, "percentaje": 0},
    )


def proyectos_usuario(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    if request:
        return render(request, "proyectos.html", {"proyectos": proyectos})
    else:
        return redirect("continuar_sesion")


def continuar_sesion(request):
    if request.user.is_authenticated:
        ultima_vista = UltimaVista.objects.filter(usuario=request.user).first()
        if ultima_vista:
            return redirect(ultima_vista.ultima_vista)
    return redirect(proyectos_usuario)
