"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from app.views.dashboard import eliminar_usuario
from app.views.formulario import generar_c_valor, generar_pdf



urlpatterns = [
    path('',views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('register/', views.register, name='register'),
    path('recuperar-contrasena/', views.recover_password, name='recoveryPassword'),
    path('continuar-sesion/', views.continuar_sesion, name='continuar_sesion'),
    path('proyectos_usuario/', views.proyectos_usuario, name='proyectos_usuario'),
    path('seleccionar/<int:id_proyecto>/', views.seleccionar , name='seleccionar'),

    #Views Form
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('info-proyecto/<int:id_proyecto>/', views.informacion_proponente, name='info_proyecto'),
    path('estructura-proyecto/<int:id_proyecto>/', views.estructura_proyecto, name='estructura_proyecto'),
    path('objetivos/<int:id_proyecto>/', views.objetivo, name='objetivos'),
    path('participantes/<int:id_proyecto>/',views.participantes, name='participantes'),
    path('seleccionar-entidad-aliada/<int:id_proyecto>/', views.selecEntidad, name='seleccionarEntidad'),
    path('proyecto/<int:id_proyecto>/entidad/<int:id_entidad>', views.parcipantes_entidad, name='part_entidad'),
    path('seleccionar-objetivo/<int:id_proyecto>/', views.selectObj, name='seleccionarObjetivo'),
    path('resultado/<int:id_proyecto>/objetivo-especifico/<int:id_objetivoEsp>/', views.producEsperados, name='producEsperados'),
    path('proyeccion/<int:id_proyecto>/', views.proyeccion, name='proyeccion'),
    path('analisis-riesgo/<int:id_proyecto>/', views.riesgo_general, name='riesgo_general'),

    #Form
    path('subir_anexos/<int:proyecto_id>/', views.subir_anexos, name='subir_anexos'),

    #Json

    # GetEditFormJson
    path('getEntidad/<int:id_entidad>/', views.getObjEspecificos, name='getObjEspecificos'),
    
    #Informacion proyecto
    path('proyecto/info-proyecto/info-proponente/<int:id_proyecto>/', views.info_proponente, name='info_proponente'),
    path('proyecto/info-proyecto/info-autor/<int:id_proyecto>/', views.info_autores, name='info-autores'),
    path('proyecto/info-proyecto/info-participante/<int:id_proyecto>/', views.info_participantes, name='info-participantes'),
    path('proyecto/info-proyecto/info-generalidades/<int:id_proyecto>/', views.info_generalidades, name='info-generalidades'),
    path('proyecto/info-proyecto/entidad_aliada/<int:id_proyecto>/', views.entidad_aliada, name='entidad_aliada'),
    path('proyecto/info-proyecto/centro-formacion/<int:id_proyecto>/', views.centro_formacion, name='centro_formacion'),
    
    #Esctructura de proyecto
    path('proyecto/est-proyecto/resumen-antecedentes/<int:id_proyecto>/', views.resumen_antecedentes, name='est_proyecto'),
    path('proyecto/est-proyecto/descripcion-problema/<int:id_proyecto>/', views.descripcion_problema, name='desc_problema'),

    #Arbol de problemas
    path('proyecto/arbol-problemas/objetivos/<int:id_proyecto>/', views.objetivos_json, name='objetivo'),
    path('proyecto/arbol-problemas/actividades/<int:id_proyecto>/', views.actividades_json, name='actividades'),

    #Analisis de riesgo
    path('proyecto/riesgos/riesgo-general/<int:id_proyecto>/', views.riesgos_obj_g_json, name='r_general'),
    path('proyecto/riesgos/riesgo-producto/<int:id_proyecto>/', views.riesgos_p_json, name='r_producto'),
    path('proyecto/riesgos/riesgo-actividad/<int:id_proyecto>/', views.riesgo_a_json, name='r_actividad'),

    #Participantes de entidad aliada
    path('proyecto/participantes-entidad/<int:id_proyecto>/', views.participantes_entidad_aliada, name='participantes_entidad'),

    #Proyeccion
    path('proyecto/proyeccion/tiempo-ejecucion/<int:id_proyecto>/', views.tiempo_ejecucion, name='tiempo_ejecucion'),
    path('proyecto/proyeccion/cadena-de-valor/<int:id_proyecto>/', views.cadena_valor, name='cadena_valor'),

    #Editar
    path('edit_proyec/<int:id_proyecto>/', views.edit_proyect, name='edit_proyec'),
    path('editar_anexo/<int:proyecto_id>/', views.editar_anexo, name='editar_anexo'),

    # PDF
    path('generar_pdf/<int:proyecto_id>/', generar_pdf, name='generar_pdf'),
    path('generar_c_valor/<int:proyecto_id>/', generar_c_valor, name='generar_c_valor'),  
    # paths admin menu
    path('Dashboard/', views.admin, name='Dashboard'),
    path('Dashboard/404/notfount/', views.not404, name='404'),
    path('Dashboard/anexosdoc/<int:proyecto_id>/', views.anexosdoc, name='anexosdoc'),
    path('Dashboard/Usuarios/', views.usuarios, name='Usuarios'),
    path('Dashboard/PreguntasPoli/', views.preguntas, name='preguntaspoli'),
    path('Dashboard/Proyectos-Inactivos/', views.proyectosINA, name='Proyecto-inactivo'),
    path('Dashboard/Proyectos-Completos/', views.proyectoT, name='Proyecto-Completo'),
    path('Dashboard/Proyectos-Pendientes', views.proyectoP, name='Proyecto-Pendiente'),
    path('eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    
    path('gantt_data/', views.gantt_data, name='gantt_data'),
    path('recursos/<int:id_proyecto>/', views.recursos, name='recursos'),
    path('proyecto/<int:id_proyecto>/recursos/cronograma/<int:id_actividad>/', views.cronogramaJson, name='cronograma'),
    path('proyecto/<int:id_proyecto>/recursos/presupuesto/<int:id_actividad>/', views.presupuestoJson, name='presupuesto'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)