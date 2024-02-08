#Funciones de ADMIN MENU

import json

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app.models import Centro_formacion, Document, Listas_plegables, Usuarios, Roles, PreguntasP
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def user_has_role(user, *roles):
    user_roles = set(user.roles.values_list('rol', flat=True))
    required_roles = set(roles)
    
    return bool(user_roles & required_roles)


@login_required(login_url='/login')
def admin(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Admin.html')

@login_required(login_url='/login')
def cantidad_usuarios(request):
    cantidad_usuarios = Usuarios.objects.exclude(pk=request.user.id).count()
    data = {'cantidad_usuarios': cantidad_usuarios}
    return JsonResponse(data)


@login_required(login_url='/login')
def usuarios(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    usuarios = Usuarios.objects.all()
    roles = Roles.objects.all()
    if request.method == 'POST':
        nuevos_roles = request.POST.getlist('roles')
        usuario = Usuarios.objects.get(id=request.POST['id_usuario'])
        usuario.roles.set(Roles.objects.filter(rol__in=nuevos_roles))
    
    return render(request, 'Dashboard/usuarios.html', {'usuarios': usuarios, 'roles': roles})



@login_required(login_url=('/login'))
def preguntas(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    contex = {
        'preguntas':PreguntasP.objects.all()
    }
    return render(request, 'Dashboard/PreguntasP.html', contex)

@login_required(login_url=('/login'))
def proyectosINA(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Proyectos-eliminados.html')

@login_required(login_url=('/login'))
def proyectoP(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Proyectos-pendientes.html')

@login_required(login_url=('/login'))
def proyectoT(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    return render(request, 'Dashboard/Proyectos-terminado.html')


@login_required(login_url=('/login'))
def register(request):
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    if request.method == 'POST':
        if Usuarios.objects.filter(email=request.POST["email"]).exists():
            msg = "Este email ya existe"
            return render(request, 'Dashboard/register.html', {'msg': msg})
        else:
            user = Usuarios.objects.create_user(email=request.POST["email"],
                                            password=request.POST["password"],
                                            username=request.POST["email"],
                                            first_name=request.POST["first_name"],
                                            last_name=request.POST["last_name"],
                                            tipo_documento=request.POST["tipo_documento"],
                                            num_documento=request.POST["num_documento"],
                                            temp_password=request.POST["password"],
                                            is_active=False)
            rol_lector = Roles.objects.get(rol='L')
            user.roles.add(rol_lector)
            user.save()
            return redirect('Usuarios')
    else:
        return render(request, 'Dashboard/register.html')
      
@login_required(login_url=('/login'))
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuarios, id=usuario_id)
    roles = list(usuario.roles.all())
    usuario.delete()
    for rol in roles:
        rol.usuarios_set.remove(usuario)
    return JsonResponse({'mensaje': 'Usuario eliminado exitosamente.'})
  
  
def act_info(request):
    return render(request, 'Dashboard/code_iv.html')


def grupos_Investigacion(request):
    if request.method == 'GET':
        # Filtra los registros que no tienen campos vacíos
        data = list(Listas_plegables.objects.exclude(
            nombre_grupo_investigacion__isnull=True,
            nombre_grupo_investigacion__exact='',
            codigos_grupo_investigacion__isnull=True,
            codigos_grupo_investigacion__exact=''
        ).values('nombre_grupo_investigacion', 'codigos_grupo_investigacion'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def redes_de_conocimiento(request):
    if request.method == 'GET':
        # Filtra los registros que no tienen campos vacíos
        data = list(Listas_plegables.objects.exclude(
            redes_conocimiento__isnull=True,
            redes_conocimiento__exact='',
        ).values('redes_conocimiento'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def subareas_de_conocimiento(request):
    if request.method == 'GET':
        data = list(Listas_plegables.objects.exclude(
            subareas_conocimiento__isnull=True,
            subareas_conocimiento__exact='',
        ).values('subareas_conocimiento'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def diciplina_de_subarea(request):
    if request.method == 'GET':
        data = list(Listas_plegables.objects.exclude(
            diciplina_subarea__isnull=True,
            diciplina_subarea__exact='',
        ).values('diciplina_subarea'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
    
def nombre_de_centro_formacion(request):
    if request.method == 'GET':
        data = list(Listas_plegables.objects.exclude(
            nombre_centro_formacion__isnull=True,
            nombre_centro_formacion__exact='',
        ).values('nombre_centro_formacion'))

        response_data = {"data": data}
        return JsonResponse(response_data, safe=False)
  
    
@csrf_exempt
def agregar_dato(request):
    if request.method == 'POST':
        try:
            campo1 = request.POST.get('campo1')
            campo2 = request.POST.get('campo2')

            registros_con_campos_vacios = Listas_plegables.objects.filter(codigos_grupo_investigacion='', nombre_grupo_investigacion='')

            if registros_con_campos_vacios.exists():
                primer_registro_con_campos_vacios = registros_con_campos_vacios.first()
                primer_registro_con_campos_vacios.nombre_grupo_investigacion = campo1
                primer_registro_con_campos_vacios.codigos_grupo_investigacion = campo2
                primer_registro_con_campos_vacios.save()
                
                print("Registro actualizado con campos vacíos.")
            else:
                print("No se encontraron registros con ambos campos vacíos.")

                nuevo_dato = Listas_plegables(nombre_grupo_investigacion=campo1, codigos_grupo_investigacion=campo2)
                nuevo_dato.save()

                print("Nuevo registro creado.")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error al agregar datos: {str(e)}')
            return JsonResponse({'status': 'error', 'error_message': str(e)})

    return JsonResponse({'status': 'error'})

@csrf_exempt
def agregar_dato2(request):
    if request.method == 'POST':
        try:
            redes_c = request.POST.get('campo1')
            registros_con_campos_vacios = Listas_plegables.objects.filter(redes_conocimiento='')

            if registros_con_campos_vacios.exists():
                primer_registro_con_campos_vacios = registros_con_campos_vacios.first()
                primer_registro_con_campos_vacios.redes_conocimiento = redes_c
                primer_registro_con_campos_vacios.save()
                
                print("Registro actualizado con campos vacíos.")
            else:
                print("No se encontraron registros con ambos campos vacíos.")

                nuevo_dato = Listas_plegables(redes_conocimiento=redes_c)
                nuevo_dato.save()

                print("Nuevo registro creado.")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error al agregar datos: {str(e)}')
            return JsonResponse({'status': 'error', 'error_message': str(e)})

    return JsonResponse({'status': 'error'})

@csrf_exempt
def agregar_dato3(request):
    if request.method == 'POST':
        try:
            subareas = request.POST.get('campo1')
            registros_con_campos_vacios = Listas_plegables.objects.filter(subareas_conocimiento='')

            if registros_con_campos_vacios.exists():
                primer_registro_con_campos_vacios = registros_con_campos_vacios.first()
                primer_registro_con_campos_vacios.subareas_conocimiento = subareas
                primer_registro_con_campos_vacios.save()
                
                print("Registro actualizado con campos vacíos.")
            else:
                print("No se encontraron registros con ambos campos vacíos.")

                nuevo_dato = Listas_plegables(subareas_conocimiento=subareas)
                nuevo_dato.save()

                print("Nuevo registro creado.")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error al agregar datos: {str(e)}')
            return JsonResponse({'status': 'error', 'error_message': str(e)})

    return JsonResponse({'status': 'error'})

@csrf_exempt
def agregar_dato4(request):
    if request.method == 'POST':
        try:
            diciplina = request.POST.get('campo1')
            registros_con_campos_vacios = Listas_plegables.objects.filter(diciplina_subarea='')

            if registros_con_campos_vacios.exists():
                primer_registro_con_campos_vacios = registros_con_campos_vacios.first()
                primer_registro_con_campos_vacios.diciplina_subarea = diciplina
                primer_registro_con_campos_vacios.save()
                
                print("Registro actualizado con campos vacíos.")
            else:
                print("No se encontraron registros con ambos campos vacíos.")

                nuevo_dato = Listas_plegables(diciplina_subarea=diciplina)
                nuevo_dato.save()

                print("Nuevo registro creado.")

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error al agregar datos: {str(e)}')
            return JsonResponse({'status': 'error', 'error_message': str(e)})

    return JsonResponse({'status': 'error'}) 

def agregar_pregunta(request):
    try:
        pregunta = PreguntasP()
        pregunta.enunciado = request.POST["iPregunta"]
        pregunta.estado = True
        pregunta.periodo = request.POST["iPeriodo"]
        pregunta.normalized = request.POST["iPregunta"]
        pregunta.save()
        new_question = {
            "id": pregunta.id,
            "enunciado": pregunta.enunciado,
            "estado": pregunta.estado,
            "periodo": pregunta.periodo,
        }
        return JsonResponse({"mensaje": "Operación exitosa", "question": new_question})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

## Estoy probando:

@login_required(login_url=('/login'))
def preguntas(request):
    documents = Document.objects.all()
    print(documents)
    if not user_has_role(request.user,'Admin'):
      return redirect('index')
    contex = {
        'documents': documents,
        'preguntas':PreguntasP.objects.all()
    }
    return render(request, 'Dashboard/PreguntasP.html', contex)


@csrf_exempt 
def guardar_anexo(request):
    if request.method == 'POST':
        nombre_anexo = request.POST.get('nombre_anexo')
        estado_anexo_str = request.POST.get('estado_anexo')
        
        # Convertir el string 'true' o 'false' a un booleano
        estado_anexo = estado_anexo_str.lower() == 'true'

        # Guardar el nuevo anexo en la base de datos
        nuevo_anexo = Document(nombre=nombre_anexo, estado=estado_anexo)
        nuevo_anexo.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
@csrf_exempt
def cargar_guia(request):
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        document = Document.objects.get(id=document_id)
        guia_file = request.FILES.get('guia')

        document.guia = guia_file
        document.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
def changeState(request, id):
    try:
        question = PreguntasP.objects.get(id=id)
        state = request.POST.get('state')
        question.estado = json.loads(state.lower())

        question.save()
        return JsonResponse({"mensaje": "Operación exitosa"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

