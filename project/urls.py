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

urlpatterns = [
    path('',views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('registrarse/', views.register, name='register'),
    path('recuperar-contrasena/', views.recover_password, name='recoveryPassword'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('info-proyecto/', views.Informacion_de_centro_view, name='info_proyecto'),
    path('autores/',views.Autores_view, name='autores'),
    #Mostrar autores
    path('ver-autores/', views.Mostrar_autores, name='mostrar_autores'),
    path('participantes/',views.Participantes_view, name='participantes'),
    #Informacion_proyecto son las "generalidades" del mismo
    path('generalidades/',views.Informacion_Proyecto_view, name='generalidades'),
    path('est-proyecto/',views.Estructura_del_proyecto_view, name='est_proyecto'),
    path('est-arbolp/',views.Estructura_arbol_problemas_view, name='est_arbolp'),
    path('est-problema/',views.Estructura_problema_view, name='est_problema'),
    path('part-proyecto/',views.Analisis_Participantes_view, name='part_proyecto'),
    path('entidad-aliada/',views.Entidades_aliadas_view, name='ent_aliada'),
    path('riesgos-proyecto/',views.Riesgos_objetivo_general_view, name='riesgos_proyecto'),
    path('riesgo-productos/',views.Riesgo_productos_view, name='riesgo_productos'),
    path('riesgo-actividades/',views.Riesgo_actividades_view, name='riesgo_actividades'),
    path('metodologia/',views.Metodologia_view, name='metodologia'),
    path('objetivos/',views.Objetivos_view, name='objetivos'),
    path('anexos/',views.Anexos_view, name='anexos'),
    path('proyeccion/',views.Proyeccion_view, name='proyeccion'),
]
