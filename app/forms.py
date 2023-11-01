# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Causa, Efecto, Objetivos, Objetivos_especificos, Proyecto, Informacion_proponente , Document , Usuarios

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

class ObjetivoEspecificoForm(forms.ModelForm):
    class Meta:
        model = Objetivos_especificos
        fields = '__all__'
        exclude = ['objetivos']

class CausaForm(forms.ModelForm):
    class Meta:
        model = Causa
        fields = '__all__'
        exclude = ['obejetivo_especifico']

class EfectoForm(forms.ModelForm):
    class Meta:
        model = Efecto
        fields = '__all__'
        exclude = ['causas']
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['anexo1', 'anexo2', 'anexo3', 'anexo4', 'anexo5', 'anexo6']
        exclude = ['proyecto']
        
class RolesForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['roles']
