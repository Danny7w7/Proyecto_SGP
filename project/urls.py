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

urlpatterns = [
    path('',views.index, name='index'),
    path('admin/', admin.site.urls),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('register/', views.register, name='register'),
    path('recuperar-contrasena/', views.recover_password, name='recoveryPassword'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('info-proyecto/<int:id_proyecto>/', views.Informacion_de_centro, name='info_proyecto'),
    # path('info-proyecto/', views.Informacion_de_centro_view, name='info_proyecto'),
    
    
    # paths admin menu
    path('Dashboard/', views.admin, name='Dashboard'),
    path('Dashboard/404/notfount/', views.not404, name='404'),
    path('Dashboard/Doc-Anexos/', views.anexosdoc, name='anexosdoc'),
    path('Dashboard/Usuarios/', views.usuarios, name='Usuarios'),
    path('Dashboard/PreguntasPoli/', views.preguntas, name='preguntaspoli'),
    path('Dashboard/Proyectos-Inactivos/', views.proyectosINA, name='Proyecto-inactivo'),
    path('Dashboard/Proyectos-Completos/', views.proyectoT, name='Proyecto-Completo'),
    path('Dashboard/Proyectos-Pendientes', views.proyectoP, name='Proyecto-Pendiente'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
