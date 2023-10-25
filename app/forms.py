# forms.py
from django import forms
from django.forms import modelformset_factory

from .models import Objetivos, Proyecto, Informacion_proponente

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        exclude = ['usuario','progress']

# Informacion proponente
class Informacion_proponenteForm(forms.ModelForm):
    class Meta:
        model = Informacion_proponente
        fields = '__all__'
        exclude = ['proyecto']
        
class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivos
        fields = '__all__'
        exclude = ['objetivo_proyecto']
