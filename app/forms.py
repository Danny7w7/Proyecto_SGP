# forms.py
from django import forms
from django.forms import modelformset_factory

from .models import Objetivos, Objetivos_especificos, Proyecto, Informacion_proponente , Document

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
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['anexo1', 'anexo2', 'anexo3', 'anexo4', 'anexo5', 'anexo6']
        exclude = ['proyecto']
        
        
class Objetivo_espeForm(forms.ModelForm):
    class Meta:
        model = Objetivos_especificos
        fields = '__all__'
        exclude = ['objetivos']