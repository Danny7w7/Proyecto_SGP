# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import Actividades_de_objetivos_especificos, Causa, Efecto, Objetivos, Objetivos_especificos, Proyecto, Informacion_proponente , Document , Usuarios, Resultados_y_productos_esperados, Participantes_entidad_alidad

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
        exclude = ['proyecto']

class ObjetivoEspecificoForm(forms.ModelForm):
    class Meta:
        model = Objetivos_especificos
        fields = '__all__'
        exclude = ['objetivos']

class ActividadEspeForm(forms.ModelForm):
    class Meta:
        model = Actividades_de_objetivos_especificos
        fields = '__all__'
        exclude = ['objetivo_especificos']

class CausaForm(forms.ModelForm):
    class Meta:
        model = Causa
        fields = '__all__'
        exclude = ['objetivo_especifico']

class EfectoForm(forms.ModelForm):
    class Meta:
        model = Efecto
        fields = '__all__'
        exclude = ['causas']

class ProducEsperados(forms.ModelForm):
    class Meta:
        model = Resultados_y_productos_esperados
        fields = '__all__'
        exclude = ['objetivo_especifico']

class ParticipantesEntidadForm(forms.ModelForm):
    class Meta:
        model = Participantes_entidad_alidad
        fields = '__all__'
        exclude = ['entidad']
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['anexo1', 'anexo2', 'anexo3', 'anexo4', 'anexo5', 'anexo6']
        exclude = ['proyecto']
        
class RolesForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['roles']
