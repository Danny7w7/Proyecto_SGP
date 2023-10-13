# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Proyecto, Autores, Participantes_Proyecto, Entidades_aliadas, RiesgoObjetivoGeneral, RiesgoProductos, RiesgoActividades 

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'