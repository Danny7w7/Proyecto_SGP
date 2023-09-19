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
    path('admin/', admin.site.urls),
    path('crear-proyecto/', views.crear_proyecto_view, name='crear_proyecto'),
    path('info-proyecto/', views.Informacion_de_centro_view, name='info_proyecto'),
    path('autores/',views.Autores_view, name='autores'),
    path('participantes/',views.Participantes_view, name='participantes'),
    #Informacion_proyecto son las "generalidades" del mismo
    path('generalidades/',views.Informacion_Proyecto_view, name='generalidades'),
]
